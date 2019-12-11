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

import time

from weboob.browser import PagesBrowser, URL, LoginBrowser, need_login
from weboob.capabilities.bank import AccountNotFound
from weboob.exceptions import BrowserIncorrectPassword
from weboob.tools.compat import basestring

from .pages import LoginPage, ListPage

__all__=['Fakebankv3Browser']
class Fakebankv3Browser(LoginBrowser,PagesBrowser):
    BASEURL = 'https://people.lan.budget-insight.com/'

    login = URL('/~ntome/fake_bank.wsgi/v3/login', LoginPage)
    accounts = URL('/~ntome/fake_bank.wsgi/v3/app',ListPage)
    home = URL('/$')
    form={}
    def go_home(self):
        self.home.go()
        assert self.home.is_here()
    def do_login(self):
        print (self.password)
        #print(f"login:{self.login}")
        self.login.stay_or_go()
        self.page.login(self.username, self.password)
        if self.login.is_here():
            raise BrowserIncorrectPassword()
    @need_login
    def iter_accounts_list(self):
        print("here")
        #self.accounts.stay_or_go()

        form1 = {'action': 'accounts'}
        self.accounts.go(data=form1)
        return self.page.iter_accounts()

    @need_login
    def iter_history(self,id):
        self.form = {'action': 'history','account_id':id,"page":"1"}
        self.accounts.go(data=self.form)
        for transaction in self.page.iter_history():
            yield transaction
