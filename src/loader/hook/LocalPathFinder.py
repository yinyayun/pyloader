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
    def __init__(self, baseurl, packInfo):
        self._links = {}
        self._baseurl = baseurl
        self._packInfo = packInfo
        self._loadedModules = set()

    def _get_pys(self, dir_path):
        links = set()
        names = os.listdir(dir_path)
        for name in names:
            if not name == ('__pycache__'):
                links.add(name)
        return links

    def find_loader(self, fullname):
        log.debug('find_loader: [%s],base is:[%s]' % (fullname, self._baseurl))
        self._loadedModules.add(fullname)
        parts = fullname.split('.')
        basename = parts[-1]
        # Check link cache
        # 说明目前正在加载子包，路径中已经含有模型名称和版本前缀
        if self._baseurl.startswith(self._packInfo.base) and self._baseurl != self._packInfo.base:
            baseurl = self._baseurl
        else:
            baseurl = self._baseurl + '/' + self._packInfo.prefix

        if baseurl not in self._links:
            self._links[baseurl] = self._get_pys(baseurl)

        # Check if it's a package
        if basename in self._links[baseurl]:
            fullurl = baseurl + '/' + basename
            # Attempt to load the package (which accesses __init__.py)
            loader = LocalPackageLoader(fullurl)
            try:
                loader.load_module(fullname)
            except ImportError:
                loader = None
            return loader, [fullurl]

        # A normal module
        filename = basename + '.py'
        if filename in self._links[baseurl]:
            return LocalModuleLoader(baseurl), []
        else:
            return None, []

    def invalidate_caches(self):
        log.debug('clear LocalPathFinder cache :%s', self._loadedModules)
        self._links = {}
        for key in self._loadedModules:
            if key in sys.modules:
                del sys.modules[key]
