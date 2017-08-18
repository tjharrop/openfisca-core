#! /usr/bin/env python
# -*- coding: utf-8 -*-


from setuptools import setup, find_packages


setup(
    name = 'OpenFisca-Core',
    version = '16.2.0',
    author = 'OpenFisca Team',
    author_email = 'contact@openfisca.org',
    classifiers = [
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Legal Industry",
        "Intended Audience :: Other Audience",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 2.7",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Software Development :: Libraries",
        ],
    description = 'Turn law into software',
    keywords = 'legal simulation tax fiscal modelling',
    license = 'AGPL-3.0',
    url = 'https://github.com/openfisca/openfisca-core',

    data_files = [
        ('share/openfisca/openfisca-core', ['CHANGELOG.md', 'LICENSE.AGPL.txt', 'README.md']),
        ],
    entry_points = {
        'console_scripts': ['openfisca-run-test=openfisca_core.scripts.run_test:main'],
        },
    extras_require = {
        'test': [
            'nose',
            'flake8',
            'openfisca-country-template == 1.2.4',
            'openfisca-extension-template == 1.1.0',
            ],
        'tracker': [
            'openfisca-tracker',
            ]
        },
    include_package_data = True,  # Will read MANIFEST.in
    install_requires = [
        'Biryani[datetimeconv] >= 0.10.4',
        'numpy >= 1.11, < 1.13',
        'PyYAML >= 3.10',
        'flask == 0.12',
        'flask-cors == 3.0.2',
        'gunicorn >= 19.7.1',
        'lxml >= 3.7',
        'dpath == 1.4.0'
        ],
    message_extractors = {
        'openfisca_core': [
            ('**.py', 'python', None),
            ],
        },
    packages = find_packages(exclude=['tests*']),
    test_suite = 'nose.collector',
    )
