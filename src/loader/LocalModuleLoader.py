'''
Created on 2018年10月26日

@author: yinyayun
'''
import _io
import imp
import importlib.abc
import logging
import os
import sys


log = logging.getLogger(__name__)
# Module Loader for Local


class LocalModuleLoader(importlib.abc.SourceLoader):
    def __init__(self, base):
        self._base = base
        self._source_cache = {}

    def module_repr(self, module):
        return '<urlmodule %r from %r>' % (module.__name__, module.__file__)

    # Required method
    def load_module(self, fullname):
        code = self.get_code(fullname)
        mod = sys.modules.setdefault(fullname, imp.new_module(fullname))
        mod.__file__ = self.get_filename(fullname)
        mod.__loader__ = self
        mod.__package__ = fullname.rpartition('.')[0]
        exec(code, mod.__dict__)
        return mod

    # Optional extensions
    def get_code(self, fullname):
        src = self.get_source(fullname)
        return compile(src, self.get_filename(fullname), 'exec')

    def get_filename(self, fullname):
        return self._base + '/' + fullname.split('.')[-1] + '.py'

    def get_data(self, path):
        pass

    # 读取文件内容
    def get_source(self, fullname):
        filename = self.get_filename(fullname)
        log.debug('loader: reading %r', filename)
        if filename in self._source_cache:
            log.debug('loader: cached %r', filename)
            return self._source_cache[filename]
        try:
            if filename.endswith('__init__.py') and not os.path.exists(filename):
                with open(filename, 'w') as _:
                    pass
            with _io.FileIO(filename, 'r') as file:
                source = file.read()
                self._source_cache[filename] = source
            log.debug('loader: %r loaded', filename)
            return source
        except Exception as e:
            log.debug('loader: %r failed. %s', filename, e)
            raise ImportError("Can't load %s" % filename)

    def is_package(self, fullname):
        return False
