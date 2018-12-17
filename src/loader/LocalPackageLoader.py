'''
Created on 2018年10月26日

@author: yinyayun
'''
from loader.LocalModuleLoader import LocalModuleLoader


class LocalPackageLoader(LocalModuleLoader):
    def load_module(self, fullname):
        mod = super().load_module(fullname)

    def get_filename(self, fullname):
        return self._base + '/' + '__init__.py'

    def is_package(self, fullname):
        return True
