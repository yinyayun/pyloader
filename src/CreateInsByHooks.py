'''
Created on 2018年10月30日

@author: yinyayun
'''

from loader.hook.DynamicLoadByHooks import DynamicLoadByHooks
if __name__ == '__main__':
    base = '../package/demo'
    dynamic = DynamicLoadByHooks(base)
    print("-----create 001.ImportDemo")
    ins1 = dynamic.create_ins('001', 'ImportDemo', 'ImportDemo')
    print(ins1.zz())
    print("-----create 002.ImportDemo")
    ins2 = dynamic.create_ins('002', 'ImportDemo', 'ImportDemo')
    print(ins2.zz())

    print('run ins1:', ins1.zz())
    print('run ins2:', ins2.zz())
