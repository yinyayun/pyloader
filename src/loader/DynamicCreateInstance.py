'''
Created on 2018年10月29日

@author: yinyayun
'''
import importlib
import sys
import threading

from loader.LocalMetaFinder import LocalMetaFinder


class PackageInfo():
    def __init__(self, base):
        self.base = base

    def setPrefix(self, prefix):
        self.prefix = prefix


class DynamicCreateInstance():
    '''
    动态创建实例，主要针对多版本的py的加载创建。
    '''

    def __init__(self, base):
        self.packageInfo = PackageInfo(base)
        self._value_lock = threading.Lock()
        self.finder = LocalMetaFinder(base, self.packageInfo)
        sys.meta_path.append(self.finder)

    def create_ins(self, prefix, moduleName, className):
        with self._value_lock:
            self.packageInfo.setPrefix(prefix)
            moudle = importlib.import_module(moduleName)
            clazz = getattr(moudle, className)
            ins = clazz()
            return ins
