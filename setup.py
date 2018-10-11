try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
import sys

from codecs import open
from os import path

if sys.version < '3.5.1':
    print("Supports only Python >= 3.5.1")
    sys.exit(1)

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='chef-cli',
    include_package_data=True,
    packages=["chefcli"],
    data_files=[('chefcli', [])],
    entry_points={'console_scripts': ['chef-cli = chefcli.__main__:main']},
    install_requires=['python-decouple', 'mdv',
                      'requests', 'termgraph', 'termcolor'],
    python_requires='>=3.5',
    requires=['decouple', 'mdv', 'requests', 'termgraph', 'termcolor'],
    version='1.0.1',
    url='https://github.com/mkfeuhrer/chef-cli',
    keywords="chef-cli codechef cli programming",
    license='MIT',
    author='Abhey Rana',
    author_email='abhey.mnnit@gmail.com',
    description='CodeChef command line interface. ChefCLI helps competitive coders to search, view,\
                 and submit problems in CodeChef.',
    long_description=long_description,
    long_description_content_type='text/markdown'
)
