# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['streamlit_cookies_manager']

package_data = \
{'': ['*'],
 'streamlit_cookies_manager': ['build/*',
                               'build/static/js/*',
                               'public/*',
                               'src/*']}

install_requires = \
['cryptography', 'streamlit>=0.84']

setup_kwargs = {
    'name': 'streamlit-cookies-manager',
    'version': '0.2.0',
    'description': 'Access and save cookies from Streamlit',
    'long_description': '# Streamlit Cookies Manager\n\nAccess and change browser cookies from Streamlit scripts:\n\n```python\nimport os\nimport streamlit as st\nfrom streamlit_cookies_manager import EncryptedCookieManager\n\n# This should be on top of your script\ncookies = EncryptedCookieManager(\n    # This prefix will get added to all your cookie names.\n    # This way you can run your app on Streamlit Cloud without cookie name clashes with other apps.\n    prefix="ktosiek/streamlit-cookies-manager/",\n    # You should really setup a long COOKIES_PASSWORD secret if you\'re running on Streamlit Cloud.\n    password=os.environ.get("COOKIES_PASSWORD", "My secret password"),\n)\nif not cookies.ready():\n    # Wait for the component to load and send us current cookies.\n    st.stop()\n\nst.write("Current cookies:", cookies)\nvalue = st.text_input("New value for a cookie")\nif st.button("Change the cookie"):\n    cookies[\'a-cookie\'] = value  # This will get saved on next rerun\n    if st.button("No really, change it now"):\n        cookies.save()  # Force saving the cookies now, without a rerun\n```\n',
    'author': 'Tomasz Kontusz',
    'author_email': 'tomasz.kontusz@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
