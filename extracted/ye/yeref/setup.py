from setuptools import setup

setup(
    name='yeref',
    version='0.24.7',
    description='desc-f',
    author='john smith',
    packages=['yeref'],
    package_data={'yeref': ['tonweb.js']},
    # install_requires=[ "aiogram>=2.22.1", ]
)

# endregion

# rm -rf dist && python -m build; twine upload --repository yeref dist/*; python3 -m pip install --upgrade yeref ; python3 -m pip install --upgrade yeref
# python3 -m pip install --upgrade yeref --break-system-packages

# python3 -m pip install --force-reinstall /Users/mark/PycharmProjects/AUTOBOT/yeref/dist/yeref-0.5.58-py3-none-any.whl
# pip install --force-reinstall -v "yeref==0.1.30"
# pip install --force-reinstall -v "pydantic[dotenv]==1.10.12"
# pip install aiogram==3.0.0b8
# pip install -U g4f==0.1.9.0

# pip install https://github.com/aiogram/aiogram/archive/refs/heads/dev-3.x.zip
# pip show aiogram
# ARCHFLAGS="-arch x86_64" pip install pycurl
