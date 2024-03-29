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

from weboob.browser import PagesBrowser, URL, LoginBrowser, need_login


from weboob.capabilities.bank import AccountNotFound


from .pages import IndexPage, ListPage, LoginPage, HistoryPage

__all__ = ['FakebankBrowser']


class FakebankBrowser(LoginBrowser, PagesBrowser):
    BASEURL = 'https://people.lan.budget-insight.com/'

    login = URL('/~ntome/fake_bank.wsgi/v1/login', LoginPage)

    home = URL('/~ntome/fake_bank.wsgi/v1/$', IndexPage)
    accounts = URL('/~ntome/fake_bank.wsgi/v1/accounts$', ListPage)
    account_url = URL('/~ntome/fake_bank.wsgi/v1/accounts/(?P<id>\d+)', HistoryPage)

    def go_home(self):
        self.home.go()
        assert self.home.is_here()

    @need_login
    def iter_accounts_list(self):
        self.accounts.stay_or_go()
        return self.page.iter_accounts()

    def do_login(self):
        self.login.stay_or_go()
        self.page.login(self.username, self.password)



    @need_login
    def get_account(self, num):
        for count, account in enumerate(self.iter_accounts_list()):
            if (count + 1) == int(num):
                return account
        raise AccountNotFound()

    @need_login
    def get_history(self, selected_account):
        # print(selected_account.url)
        self.account_url.go(id=selected_account.id)
        for transaction in self.page.iter_history():
            yield transaction


