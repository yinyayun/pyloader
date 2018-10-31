'''
Created on 2018年10月26日

@author: yinyayun
'''


from loader.DynamicCreateInstance import DynamicCreateInstance


if __name__ == '__main__':
    base = '../package/demo'
    dynamicCreateInstance = DynamicCreateInstance(base)
    print("#########加载001###########")
    print('----------------------')
    v1 = dynamicCreateInstance.create_ins('001', 'ImportDemo', 'ImportDemo')
    print("=======", v1.zz())
