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

from weboob.browser.filters.json import Dict

from weboob.browser.pages import  HTMLPage, JsonPage

from weboob.browser.filters.standard import CleanText, CleanDecimal, Date
from weboob.capabilities import NotAvailable
from weboob.capabilities.bank import Account, Transaction
from weboob.browser.elements import method, ItemElement, DictElement, TableElement

__all__ = ['AccountPage','LoginPage', 'HistoryPage']
class LoginPage(HTMLPage):

    def get_token(self):
        return self.doc['detail']['token']

    def login(self, username, password):

        json_data = {
            'login': username,
            'password': password
        }
        print(username, password)
        self.browser.location('https://people.lan.budget-insight.com/~ntome/fake_bank.wsgi/v2/login.json',
                              data=json_data, method='POST')


class AccountPage(JsonPage):
    @method
    class get_accounts(DictElement):
        item_xpath = 'accounts'

        class item(ItemElement):
            klass = Account
            obj_id = CleanText(Dict('id'))
            obj_label = CleanText(Dict('label'))
            obj_balance = CleanText(Dict('balance'))

class HistoryPage(JsonPage):
    @method
    class get_history(DictElement):

        item_xpath = "transactions"
        class item(ItemElement):
            klass = Transaction
            obj_date = Date(CleanText(Dict("date")))
            obj_label = CleanText(Dict("label"))
            obj_amount= CleanDecimal(Dict("amount"))
