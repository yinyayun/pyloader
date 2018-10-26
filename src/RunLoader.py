'''
Created on 2018年10月26日

@author: yinyayun
'''
import loader.LocalMetaFinder as load
load.install_meta('../pys')
moudle = __import__("ImportDemo")
clazz = getattr(moudle, 'ImportDemo')
print(clazz().zz())
