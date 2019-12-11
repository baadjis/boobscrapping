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


from weboob.tools.backend import Module, BackendConfig
from weboob.capabilities.bank import CapBank
from weboob.tools.capabilities.bank.transactions import sorted_transactions
from weboob.tools.value import ValueBackendPassword, Value

from .browser import Fakebankv2Browser


__all__ = ['Fakebankv2Module']


class Fakebankv2Module(Module, CapBank):
    NAME = 'fakebankv2'
    DESCRIPTION = 'fakebankv2 website'
    MAINTAINER = 'baadjis'
    EMAIL = 'baadjisidy@gmail.com'
    LICENSE = 'LGPLv3+'
    VERSION = '1.6'


    BROWSER = Fakebankv2Browser

    CONFIG = BackendConfig(Value('login', label='Username', regexp='.+', default='foo'),
                           ValueBackendPassword('password', label='Password', default='bar'),
                           )


    def create_default_browser(self):
        print(self.config['login'].get())
        print(self.config['password'].get())

        return self.create_browser(self.config['login'].get(), self.config['password'].get())

    def iter_accounts(self):
        for account in self.browser.get_accounts_list():
            yield account
    def iter_history(self, account):
        transactions = sorted_transactions(self.browser.get_history(account))
        return transactions
