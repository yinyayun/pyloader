实现python文件的动态加载，包括对主module中依赖的一些文件的查找加载。

Python动态加载实现方案：
- sys.path.append(),即将要加载的目录放入系统搜索路径列表。但是无法定制化加载。
- 实现finder和loader
- 添加钩子函数，为指定目录绑定finder

关于测试动态加载module目录结构(`/package/demo`） 说明
（1）001和002为不同版本的实现
（2）文件结构和文件名称都一致，唯一不同是sub.SubDenpendence.py的实现
（3）ImportDemo依赖DenpendenceDemo，DenpendenceDemo依赖SubDenpendence
(4)系统查找的基础路径为package/demo
（5）py文件的中module基路径与sub同级

为了能够进行module的多版本加载，使用第二种和第三种都是可行的，但是第三种更为方便一点，该方便主要在从sys.modules中清除已经缓存的module。

具体的不多说，还是看代码吧。

基于路径钩子实现的程序运行入口：`CreateInsByHooks.py`
基于钩子实现对应路径解析finder参见：`LocalPathFinder.py`:


