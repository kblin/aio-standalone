import os
import sys
from setuptools import setup
from setuptools.command.test import test as TestCommand


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


short_description = "Standalone application server framework using asyncio"
long_description = read('README.md')

install_requires: list[str] = []


tests_require = [
    'pytest',
    'coverage',
    'pytest-cov',
    'pytest-asyncio',
]


def read_version():
    for line in open(os.path.join('aiostandalone', '__init__.py'), 'r'):
        if line.startswith('__version__'):
            return line.split('=')[-1].strip().strip("'")


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)


setup(
    name='aio-standalone',
    version=read_version(),
    author='Kai Blin',
    author_email='kblin@biosustain.dtu.dk',
    description=short_description,
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=install_requires,
    tests_require=tests_require,
    cmdclass={'test': PyTest},
    packages=['aiostandalone'],
    url='https://github.com/kblin/aio-standalone/',
    license='Apache Software License',
    classifiers=[
        'Programming Language :: Python',
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],
    extras_require={
        'testing': tests_require,
    },
)
