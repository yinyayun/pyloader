'''
Created on 2018年10月30日

@author: yinyayun
'''
import importlib
import logging
import os
import sys

from loader.LocalModuleLoader import LocalModuleLoader
from loader.LocalPackageLoader import LocalPackageLoader


log = logging.getLogger(__name__)


class LocalPathFinder(importlib.abc.PathEntryFinder):
    def __init__(self, base, packInfo):
        self._locals = {}
        self._base = base
        self._packInfo = packInfo
        self._loadedModules = set()

    def _get_pys(self, dir_path):
        locals = set()
        names = os.listdir(dir_path)
        for name in names:
            if not name == ('__pycache__'):
                locals.add(name)
        return locals

    def find_loader(self, fullname):
        log.debug('find_loader: [%s],base is:[%s]' % (fullname, self._base))
        self._loadedModules.add(fullname)
        parts = fullname.split('.')
        basename = parts[-1]
        # Check link cache
        # 说明目前正在加载子包，路径中已经含有模型名称和版本前缀
        if self._base.startswith(self._packInfo.base) and self._base != self._packInfo.base:
            base = self._base
        else:
            base = self._base + '/' + self._packInfo.prefix

        if base not in self._locals:
            self._locals[base] = self._get_pys(base)

        # Check if it's a package
        if basename in self._locals[base]:
            full = base + '/' + basename
            # Attempt to load the package (which accesses __init__.py)
            loader = LocalPackageLoader(full)
            try:
                loader.load_module(fullname)
            except ImportError:
                loader = None
            return loader, [full]

        # A normal module
        filename = basename + '.py'
        if filename in self._locals[base]:
            return LocalModuleLoader(base), []
        else:
            return None, []

    def invalidate_caches(self):
        log.debug('clear LocalPathFinder cache :%s', self._loadedModules)
        self._locals = {}
        for key in self._loadedModules:
            if key in sys.modules:
                del sys.modules[key]
