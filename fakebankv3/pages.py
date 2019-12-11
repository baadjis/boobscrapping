# -*- coding: utf-8 -*-

# Copyright(C) 2019      baadjis
#
# This file is part of a weboob module.
#
# This weboob module is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This weboob module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this weboob module. If not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals

import re
import tempfile

import requests
from weboob.browser.elements import ItemElement, method, TableElement, ListElement, DictElement
import math
from io import BytesIO
from random import random

from weboob.browser.filters.html import Attr, Link
from weboob.browser.filters.json import Dict
from weboob.browser.filters.standard import CleanText, Regexp, Type, CleanDecimal, Date
from weboob.capabilities.bank import Account, Transaction
from weboob.tools.captcha.virtkeyboard import MappedVirtKeyboard, VirtKeyboardError
from weboob.browser.pages import HTMLPage, FormNotFound, LoggedPage, pagination

__all__ = ['ListPage', 'LoginPage']


class fakekebankvKeyboard(MappedVirtKeyboard):
    symbols = {
        '0': '512beeec87eb71b9dbb85c694e8ce980',
        '1': 'f8876ad577c3e5c6b4b96ecad8bd06ad',
        '2': '7e9d75f5a87fb71a77159acd8b0dd754',
        '3': '0dc5f23be16202f3bbd0814b5ee68691',
        '4': '87b544a64a1f4599311571e005d2ba30',
        '5': '331fb5f2eb94bc9bb81d81d9c80f59c5',
        '6': '30bfbada7bc01231097e0c1629e890ab',
        '7': '1dd1c48a32ba74b6c573a701642ceff3',
        '8': 'a44422c9bd07bea52297525ddd6906ea',
        '9': '66d3f4f96ca332511584af8a6c3f7837'
    }
    url = "/~ntome/fake_bank.wsgi/v3/login"
    codesep = ','
    color = (255, 255, 255)

    def __init__(self, basepage):
        print(self.symbols)
        print(basepage)
        img = basepage.doc.xpath("/html/body/fieldset/form/img")[0]
        imurl = img.attrib.get("src")
        super(fakekebankvKeyboard, self).__init__(
            BytesIO(basepage.browser.open(imurl).content),
            basepage.doc, img, self.color, "href", "RGB")
        self.check_symbols(self.symbols, basepage.browser.responses_dirname)

    def get_string_code(self, string):
        return super(fakekebankvKeyboard, self).get_string_code(string) + self.codesep


class LoginPage(HTMLPage):
    def get_token(self):
        return self.doc['detail']['token']

    def on_load(self):
        try:
            form = self.get_form(xpath='/html/body/fieldset/form')
        except FormNotFound:
            return

    def login(self, username, passwd):
        try:
            vk = fakekebankvKeyboard(self)
        except VirtKeyboardError as err:
            self.logger.exception(err)
            return False

        password = vk.get_string_code(passwd)

        form = self.get_form(xpath='/html/body/fieldset/form')
        form['login'] = username
        form['code'] = password

        print(form['code'])
        print(form['login'])
        form.submit()


class ListPage(LoggedPage, HTMLPage):
    # is_here = '//div[@class="account"]'

    @method
    class iter_accounts(ListElement):
        item_xpath = '/html/body/div/div'

        class item(ItemElement):
            klass = Account

            def obj_id(self):
                a = self.el.xpath('./a')[0]
                id = re.findall(r"\d+", a.attrib.get("onclick"))[0]

                return id

            obj_label = CleanText('./a/text()')
            obj_balance = CleanDecimal('./text()')

            def obj_url(self):
                return (u'%s%s' % (self.page.browser.BASEURL, Link(u'.//a[1]')(self)))

    @pagination
    @method
    class iter_history(DictElement):

        def find_elements(self):

            add_scripts = '/html/body/script[3]'

            transactions = [el.text_content().split(';') for el in self.el.xpath(add_scripts)]

            for transaction in transactions:

                for transaction_line in transaction:
                    v = re.search(r"\nadd_transaction\((?P<content>.+)\)", transaction_line)
                    if v is not None:
                        key_values = v.group('content').split(',')
                        yield {'label': key_values[0].replace('"', ''), "date": key_values[1].replace('"', ''),
                               "amount": key_values[2]}

        class item(ItemElement):
            klass = Transaction

            obj_amount = CleanDecimal(Dict('amount'), replace_dots=True)
            obj_label = CleanText(Dict('label'))
            obj_date = Date(CleanText(Dict('date')))

        def next_page(self):
            if Link(u'//a[text()="▶"]')(self) is not None:

                form = self.page.get_form(xpath='//*[@id="history_form"]')

                form['page'] = CleanDecimal(Link(u'//a[text()="▶"]'))(self)


                return requests.Request("POST", self.page.url, data=form)

