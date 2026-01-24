from setuptools import setup, find_packages

setup(
    name='fastchat',
    version='0.1.0',
    author='Li Ding',
    author_email='213193509seu@gmail.com',
    url='https://blog.dingli.life',
    packages=find_packages(include=['fastchat', 'fastchat.*']),  # 只包括fastchat及其所有子包
    license='MIT',
    description='fastchat with guidance support',
    install_requires=[
        # 您的依赖项
    ],
    classifiers=[
        # 您的分类器
    ],
)
