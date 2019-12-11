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

from weboob.browser.elements import ItemElement, method, TableElement
from weboob.browser.filters.standard import CleanText, CleanDecimal, Regexp, Type, Async, Date, Env, TableCell
from weboob.browser.pages import HTMLPage, LoggedPage, pagination
from weboob.capabilities.bank import Account, Transaction
from weboob.browser.filters.html import Attr, Link
from weboob.capabilities.base import Field, NotAvailable

__all__ = ['IndexPage', 'ListPage', 'LoginPage', 'HistoryPage']

from weboob.tools.capabilities.bank.transactions import FrenchTransaction


class IndexPage(HTMLPage):
    pass


class ListPage(LoggedPage, HTMLPage):
    @method
    class iter_accounts(TableElement):
        head_xpath = '/html/body/table/thead'
        item_xpath = '/html/body/table/tbody/tr'

        class item(ItemElement):
            klass = Account

            obj_id = Regexp(Attr('.//a', 'href'), r'(\d+)') & Type(type=int)
            obj_label = CleanText('./td[1]')
            obj_balance = CleanDecimal('./td[2]', replace_dots=True)

            def obj_url(self):
                return (u'%s%s' % (self.page.browser.BASEURL, Link(u'.//a[1]')(self)))


class HistoryPage(LoggedPage, HTMLPage):
    @pagination
    @method
    class iter_history(TableElement):
        head_xpath = '/html/body/table/thead'
        item_xpath = '/html/body/table/tbody/tr'

        def next_page(self):
            pagenext = (u'%s%s' % (self.page.browser.url.split('?', 1)[0], Link(u'//a[text()="▶"]')(self)))

            return pagenext

        class item(ItemElement):
            klass = FrenchTransaction

            obj_date =klass.Date('./td[1]')
            obj_amount = klass.Amount('./td[3]', './td[4]')

            obj_label = CleanText('./td[2]')


class LoginPage(HTMLPage):
    def login(self, username, password):
        form = self.get_form(xpath='/html/body/fieldset/form')
        form['login'] = username
        form['password'] = password
        form.submit()
