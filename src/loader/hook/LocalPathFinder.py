'''
Created on 2018年10月26日

@author: yinyayun
'''
import importlib
import logging
import os
import sys

from loader.LocalModuleLoader import LocalModuleLoader


log = logging.getLogger(__name__)


class LocalPathFinder(importlib.abc.PathEntryFinder):
    def __init__(self, base):
        self._links = None
        self._loader = LocalModuleLoader(base)
        self._base = base

    def _get_pys(self, dir_path):
        links = set()
        names = os.listdir(dir_path)
        for name in names:
            if not name == ('__pycache__'):
                links.add(name)
        return links

    def find_loader(self, fullname):
        log.debug('find_loader: %r', fullname)
        parts = fullname.split('.')
        basename = parts[-1]
        # Check link cache
        if self._links is None:
            self._links = []  # See discussion
            self._links = self._get_pys(self._baseurl)

        # Check if it's a package
        if basename in self._links:
            log.debug('find_loader: trying package %r', fullname)
            fullurl = self._base + '/' + basename
            # Attempt to load the package (which accesses __init__.py)
            loader = LocalModuleLoader(fullurl)
            try:
                loader.load_module(fullname)
                log.debug('find_loader: package %r loaded', fullname)
            except ImportError as e:
                log.debug('find_loader: %r is a namespace package', fullname)
                loader = None
            return (loader, [fullurl])

        # A normal module
        filename = basename + '.py'
        if filename in self._links:
            log.debug('find_loader: module %r found', fullname)
            return (self._loader, [])
        else:
            log.debug('find_loader: module %r not found', fullname)
            return (None, [])

    def invalidate_caches(self):
        log.debug('invalidating link cache')
        self._links = None


# Check path to see if it looks like a URL
_url_path_cache = {}




def install_path_hook(address):
    sys.path_hooks.append(address)
    sys.path_importer_cache.clear()
    log.debug('Installing handle_url')


def remove_path_hook(address):
    sys.path_hooks.remove(address)
    sys.path_importer_cache.clear()
    log.debug('Removing handle_url')
