from setuptools import setup

with open("README.md", 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='eng_to_ipa',
    version='0.0.2',
    description='take English text and convert it to IPA',
    author=['mphilli', 'Mitchellpkt', 'CanadianCommander', 'timvancann'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    include_package_data=True,
    packages=['eng_to_ipa'],
)
