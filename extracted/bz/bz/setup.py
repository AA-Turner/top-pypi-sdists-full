from distutils.core import setup
setup(
    name='bz', # 对外我们模块的名字
    version='1.0', # 版本号
    description='这是第一个对外发布的模块，测试哦',#描述 #
    author='liupu', # 作者
    author_email='909719791@qq.com',
    py_modules=['bz.a'] # 要发布的模块
)