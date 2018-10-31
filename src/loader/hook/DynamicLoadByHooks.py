'''
Created on 2018年10月30日

@author: yinyayun
'''
import importlib
import logging
import sys
import threading

from loader.hook.LocalPathFinder import LocalPathFinder


log = logging.getLogger(__name__)


class PackageInfo():
    def __init__(self, base):
        self.base = base

    def setPrefix(self, prefix):
        self.prefix = prefix


class DynamicLoadByHooks():
    '''
    动态创建实例，主要针对多版本的py的加载创建。
     基于路径钩子实现
    '''

    def __init__(self, base):
        self._url_path_cache = {}
        self.packageInfo = PackageInfo(base)

        def handle_path(path):
            if path.startswith(base):
                log.debug('handle path:%s', path)
                if path in self._url_path_cache:
                    finder = self._url_path_cache[path]
                else:
                    finder = LocalPathFinder(path, self.packageInfo)
                    self._url_path_cache[path] = finder
                return finder
            else:
                #使得后续的钩子函数可以介入处理
                raise ImportError('can not hand path:%s' % path)

        self._value_lock = threading.Lock()
        sys.path_hooks.insert(0, handle_path)
        sys.path.append(base)

    def create_ins(self, prefix, moduleName, className):
        try:
            self._value_lock.acquire()
            self.packageInfo.setPrefix(prefix)
            moudle = importlib.import_module(moduleName)
            clazz = getattr(moudle, className)
            return clazz()
        finally:
            importlib.invalidate_caches()
            self._value_lock.release()
