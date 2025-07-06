try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

long_desc = '''Translates JavaScript to Python code. Js2Py is able to translate and execute virtually any JavaScript code.

Js2Py is written in pure python and does not have any dependencies. Basically an implementation of JavaScript core in pure python.


    import js2py

    f = js2py.eval_js( "function $(name) {return name.length}" )

    f("Hello world")

    # returns 11

Now also supports ECMA 6 through js2py.eval_js6(js6_code)!

More examples at: https://github.com/PiotrDabkowski/Js2Py
'''



# rm -rf dist build && python3 setup.py sdist bdist_wheel
# twine upload dist/*
setup(
    name='Js2Py_3.13',
    version='0.74.1',

    packages=['js2py_', 'js2py_.utils', 'js2py_.prototypes', 'js2py_.translators',
              'js2py_.constructors', 'js2py_.host', 'js2py_.es6', 'js2py_.internals',
              'js2py_.internals.prototypes', 'js2py_.internals.constructors', 'js2py_.py_node_modules'],
    url='https://github.com/PiotrDabkowski/Js2Py',
    install_requires = ['tzlocal>=1.2', 'six>=1.10', 'pyjsparser>=2.5.1'],
    license='MIT',
    author='Piotr Dabkowski',
    author_email='piodrus@gmail.com',
    description='JavaScript to Python Translator & JavaScript interpreter written in 100% pure Python.',
    long_description=long_desc
)
