# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name="OpenFisca-UK",
    version="0.2.2",
    author="UBI Center",
    author_email="nikhil.woodruff@ubicenter.org",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Topic :: Scientific/Engineering :: Information Analysis",
    ],
    description="OpenFisca tax and benefit system for UK",
    keywords="benefit microsimulation social tax",
    license="http://www.fsf.org/licensing/licenses/agpl-3.0.html",
    url="https://github.com/nikhilwoodruff/openfisca-uk",
    include_package_data=True,  # Will read MANIFEST.in
    data_files=[
        (
            "share/openfisca/openfisca-country-template",
            ["CHANGELOG.md", "LICENSE", "README.md"],
        ),
    ],
    install_requires=[
        "pandas==1.1.4",
        "numpy==1.17.5",
        "pyyaml==5.3.1",
        "pytest==5.4.3",
        "OpenFisca-Core @ git+https://github.com/nikhilwoodruff/openfisca-core",
    ],
    extras_require={
        "dev": [
            "autopep8 ==1.5",
            "flake8 >=3.5.0,<3.8.0",
            "flake8-print",
            "pycodestyle >=2.3.0,<2.6.0",  # To avoid incompatibility with flake
            "frs==0.0.1",
        ]
    },
    packages=find_packages(),
)
