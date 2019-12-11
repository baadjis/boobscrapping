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



from weboob.browser import LoginBrowser, URL
from weboob.exceptions import BrowserIncorrectPassword

from .pages import LoginPage, AccountPage ,HistoryPage
from weboob.browser import need_login


class Fakebankv2Browser(LoginBrowser):
    BASEURL = 'https://people.lan.budget-insight.com/~ntome/fake_bank.wsgi'

    login = URL(r'https://people.lan.budget-insight.com/~ntome/fake_bank.wsgi/v2/#login', LoginPage)
    accounts = URL(r'https://people.lan.budget-insight.com/~ntome/fake_bank.wsgi/v2/accounts.json', AccountPage)
    history=URL(r'https://people.lan.budget-insight.com/~ntome/fake_bank.wsgi/v2/accounts/(?P<id>\d+).json', HistoryPage)


    def __init__(self, username, password, *args, **kwargs):
        super().__init__(username, password, *args, **kwargs)
        self.home = None

    def do_login(self):
        self.login.stay_or_go()
        r=self.page.login(self.username, self.password)
        print("login",r)



    def go_home(self):
        self.home.go()

        assert self.home.is_here()

    @need_login
    def get_accounts_list(self):
        self.accounts.stay_or_go()
        print(self.page.get('accounts'))
        return self.page.get_accounts()
    @need_login
    def get_history(self,account):
        self.history.stay_or_go(id = account.id)
        print(self.page.get("history"))
        return self.page.get_history(account)
