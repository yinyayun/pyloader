'''
Created on 2018年10月26日

@author: yinyayun
'''
import importlib.abc
import logging
import os
import sys

from loader.LocalModuleLoader import LocalModuleLoader
from loader.LocalPackageLoader import LocalPackageLoader


log = logging.getLogger(__name__)


class LocalMetaFinder(importlib.abc.MetaPathFinder):
    def __init__(self, base):
        self._base = base
        self._locals = {}
        self._loaders = {base: LocalModuleLoader(base)}

    def _get_pys(self, dir_path):
        links = set()
        names = os.listdir(dir_path)
        for name in names:
            if not name == ('__pycache__'):
                links.add(name)
        return links

    def find_module(self, fullname, path=None):
        log.debug('find_module: fullname=%r, path=%r', fullname, path)
        if path is None:
            base = self._base
        else:
            if not path[0].startswith(self._base):
                return None
            base = path[0]
        parts = fullname.split('.')
        basename = parts[-1]
        log.debug('find_module: baseurl=%r, basename=%r', base, basename)

        # Check link cache
        if basename not in self._locals:
            self._locals[base] = self._get_pys(base)

        # 检测是否为一个包
        if basename in self._locals[base]:
            log.debug('find_module: trying package %r', fullname)
            fullpath = self._base + '/' + basename
            # Attempt to load the package (which accesses __init__.py)
            loader = LocalPackageLoader(fullpath)
            try:
                loader.load_module(fullname)
                self._locals[fullpath] = self._get_pys(fullpath)
                self._loaders[fullpath] = LocalModuleLoader(fullpath)
                log.debug('find_module: package %r loaded', fullname)
            except ImportError as e:
                log.debug('find_module: package failed. %s', e)
                loader = None
            return loader
        # 如果为Python文件
        filename = basename + '.py'
        if filename in self._locals[base]:
            log.debug('find_module: module %r found', fullname)
            return self._loaders[base]
        else:
            log.debug('find_module: module %r not found', fullname)
            return None

    def invalidate_caches(self):
        log.debug('invalidating link cache')
        self._locals.clear()


_installed_meta_cache = {}


def install_meta(address):
    if address not in _installed_meta_cache:
        finder = LocalMetaFinder(address)
        _installed_meta_cache[address] = finder
        sys.meta_path.append(finder)


def remove_meta(address):
    if address in _installed_meta_cache:
        finder = _installed_meta_cache.pop(address)
        sys.meta_path.remove(finder)
