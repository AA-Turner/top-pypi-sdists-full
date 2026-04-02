# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['js_routes',
 'js_routes._scripts',
 'js_routes.conf',
 'js_routes.management',
 'js_routes.management.commands',
 'js_routes.templatetags',
 'js_routes.test',
 'js_routes.utils']

package_data = \
{'': ['*'],
 'js_routes': ['static/js/routes/*',
               'templates/js_routes/*',
               'templates/js_routes/_base/*',
               'templates/js_routes/_dump/*']}

install_requires = \
['django>=3.2']

setup_kwargs = {
    'name': 'django-js-routes',
    'version': '0.2.0',
    'description': 'Expose and perform reverse lookups of Django URLs in the frontend world.',
    'long_description': 'django-js-routes\n################\n\n**Django-js-routes** is a Django application allowing to expose and perform reverse lookups of\nDjango named URL patterns on the client side.\n\n.. contents:: Table of Contents\n    :local:\n\nMain requirements\n=================\n\nPython 3.6+, Django 3.2+.\n\nInstallation\n============\n\nTo install Django-js-routes, please use the pip_ command as follows:\n\n.. code-block:: shell\n\n    $ pip install django-js-routes\n\nOnce the package is installed, you\'ll have to add the application to ``INSTALLED_APPS`` in your\nproject\'s settings module:\n\n.. code-block:: python\n\n    INSTALLED_APPS = (\n        # all other apps...\n        \'js_routes\',\n    )\n\nYou can then define which URL patterns or URL namespaces you want to expose to the client side by\nsetting the ``JS_ROUTES_INCLUSION_LIST`` setting. This setting allows to define which URLs should be\nserialized and made available to the client side through the generated and / or exported Javascript\nhelper. This list should contain only URL pattern names or namespaces. Here is an example:\n\n.. code-block:: python\n\n    JS_ROUTES_INCLUSION_LIST = [\n        \'home\',\n        \'catalog:product_list\',\n        \'catalog:product_detail\',\n    ]\n\nNote that if a namespace is included in this list, all the underlying URLs will be made available to\nthe client side through the generated Javascript helper. Django-js-routes is safe by design in the\nsense that *only* the URLs that you configure in this inclusion list will be publicly exposed on the\nclient side.\n\nOnce the list of URLs to expose is configured, you can add the ``{% js_routes %}`` tag to your base\ntemplate in order to ensure that the Javascript helper is available to you when you need it:\n\n.. code-block:: html\n\n    {% load js_routes_tags %}\n    <html>\n        <head>\n        </head>\n        <body>\n            <!-- At the bottom of the document\'s body... -->\n            {% js_routes %}\n        </body>\n    </html>\n\nUsage\n=====\n\nThe URL patterns you configured through the ``JS_ROUTES_INCLUSION_LIST`` setting can then be\nreversed using the generated ``window.reverseUrl`` function, which can be used pretty much the\n"same" way you\'d use `reverse <https://docs.djangoproject.com/en/dev/ref/urlresolvers/#reverse>`_ on\nthe Django side:\n\n.. code-block:: javascript\n\n    window.reverseUrl(\'home\');\n    window.reverseUrl(\'catalog:product_list\');\n    window.reverseUrl(\'catalog:product_detail\', productId);\n    window.reverseUrl(\'catalog:product_detail\', { pk: productId });\n\nSettings\n========\n\nJS_ROUTES_INCLUSION_LIST\n------------------------\n\nDefault: ``[]``\n\nThe ``JS_ROUTES_INCLUSION_LIST`` setting allows to define the URL patterns and URL namespaces that\nshould be exposed to the client side through the generated Javascript helper.\n\nAdvanced features\n=================\n\nInserting only the serialized URLs in Django templates\n------------------------------------------------------\n\nBy default, the ``{% js_routes %}`` template tag only allows to trigger the generation of the\nserialized URLs (which are stored in a Javascript object on the ``window`` object) and to include a\nJavascript URL resolver function in your HTML using the Django\'s\n`static <https://docs.djangoproject.com/en/dev/ref/templates/builtins/#static>`_ template tag.\nActually, a standard use of the ``{% js_routes %}`` statement is equivalent to:\n\n.. code-block:: html\n\n    {% js_routes routes_only=True %}\n    <script src="{% static \'js/routes/resolver.js\' %}"></script>\n\nThe ``routes_only`` option allows to only include the serialized URLs in the output of\n``{% js_routes %}``. It gives you the ability to include the Javascript URL resolver that comes with\nDjango-js-routes using another ``static`` statement. This also allows you to cache the output of the\n``{% js_routes routes_only=True %}`` statement if you want (so that serialized URLs are not\ngenerated for every request).\n\nDumping the Javascript routes resolver\n--------------------------------------\n\nAs explained earlier, the ``{% js_routes %}`` template tag triggers the generation of the serialized\nURLs and includes a client-side URL resolver in the final HTML. One downside of this behaviour is\nthat the serialized URLs need to be generated every time your HTML template is rendered.\n\nInstead it is possible to just dump the whole list of serialized URLs AND the URL resolver function\ninto a single Javascript module file. This can be achieved using the ``dump_routes_resolver``\ncommand, which can be used as follows:\n\n.. code-block:: shell\n\n    $ python manage.py dump_routes_resolver --format=default --output=my_exported_resolver.js\n\nThe ``--output`` option allows to specify to which file the serialized routes and resolver function\nshould be saved while the ``--format`` option allows to specify the Javascript format to use.\n\n``--format`` accepts the following values:\n\n* ``default`` includes the routes as an object that is associated to the ``window`` object while the\n  URL resolver is available through the ``window.reverseUrl`` function (this corresponds to the\n  behaviour provided by a standard use of the ``{% js_routes %}`` template tag)\n* ``es6`` allows to save the routes and the URL resolver as an ES6 module where the ``reverseUrl``\n  function is the default export\n\nLicense\n=======\n\nMIT. See ``LICENSE`` for more details.\n\n.. _pip: https://github.com/pypa/pip\n',
    'author': 'Morgan Aubert',
    'author_email': 'me@morganaubert.name',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ellmetha/django-js-routes',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
