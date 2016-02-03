from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='gappspy',
    version='0.0.1',
    description='GappsPy',
    long_description=long_description,
    url='https://github.com/fabiogibson/gappspy',
    author='Fabio Gibson',
    author_email='fabiogibson@hotmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7'
    ],
    keywords='Google Apps, Google Mail, Google Drive.',
    packages=find_packages(),
    install_requires=['google-api-python-client==1.4.2', 'pycrypto==2.6.1', 'pyopenssl'],
    extras_require={},
    package_data={},
    data_files=[],
    entry_points={},
)
