# coding: utf-8


import os
import re

from setuptools import setup, Command, find_packages

here = os.path.abspath(os.path.dirname(__file__))

version = "0.0.0"
with open(os.path.join(here, "CHANGES.txt")) as changes:
    for line in changes:
        version = line.strip()
        if re.search('^[0-9]+\.[0-9]+(\.[0-9]+)?$', version):
            break


class VersionCommand(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    # noinspection PyMethodMayBeStatic
    def run(self):
        print(version)


setup(
    name='celerytestworker',
    version=version,
    description='Control (start/stop) a Celery standalone worker for running test purpose',
    author="Osvaldo Santana Neto", author_email="celerytestworker@osantana.me",
    license="MIT",
    packages=find_packages(exclude=['tests']),
    platforms='any',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ],
    install_requires=[
        "celery",
    ],
    keywords='testing test server',
    url='http://github.com/osantana/celerytestworker',
    download_url='https://github.com/osantana/celerytestworker/tarball/{}'.format(version),
    cmdclass={'version': VersionCommand},
    test_suite="tests",
)
