'''
Created on 2018年10月28日

@author: yinyayun
'''
import importlib.abc
import logging
import os

from loader.LocalModuleLoader import LocalModuleLoader
from loader.LocalPackageLoader import LocalPackageLoader


log = logging.getLogger(__name__)


class LocalMetaFinder(importlib.abc.MetaPathFinder):
    def __init__(self, base, packageInfo):
        self._base = base
        self._locals = {}
        self._modelInfo = packageInfo
        self._loaders = {base: LocalModuleLoader(base)}

    def _get_pys(self, dir_path):
        links = set()
        names = os.listdir(dir_path)
        for name in names:
            if not name == ('__pycache__'):
                links.add(name)
        return links

    def find_module(self, fullname, path=None):
        parts = fullname.split('.')
        basename = parts[-1]
        # 如果base目录不是原初的基础目录，则需要追加模型名称和版本号
        if self._base == self._modelInfo.base:
            base = self._base + '/' + self._modelInfo.prefix
        else:
            base = self._base
        # 获取base目录下所有文件
        if base not in self._locals:
            self._locals[base] = self._get_pys(base)
        # 检测是否为一个包
        if basename in self._locals[base]:
            fullpath = base + '/' + basename
            # Attempt to load the package (which accesses __init__.py)
            loader = LocalPackageLoader(fullpath)
            try:
                loader.load_module(fullname)
                self._loaders[fullpath] = LocalModuleLoader(fullpath)
                log.debug('find_module: package %r loaded', fullname)
            except ImportError as e:
                log.debug('find_module: package failed. %s', e)
                loader = None
            return loader
        # 如果为Python文件
        filename = basename + '.py'
        if filename in self._locals[base]:
            if base not in self._loaders:
                self._loaders[base] = LocalModuleLoader(base)
            return self._loaders[base]
        else:
            return None

    def invalidate_caches(self):
        log.debug('invalidating link cache')
        self._locals.clear()
