
import io
import setuptools

with io.open('README.md', encoding='utf8') as fp:
  readme = fp.read()

setuptools.setup(
  name = 'pyinvoke',
  version = '1.0.4',
  license = 'MIT',
  long_description = readme,
  long_description_content_type = 'text/markdown',
  url = 'https://github.com/NiklasRosenstein/pyinvoke',
  author = 'Niklas Rosenstein',
  author_email = 'rosensteinniklas@gmail.com',
  py_modules = ['pyinvoke']
)
