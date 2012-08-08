try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

install_requires = ["Trac==0.12.3"]

try:
    import argparse
except ImportError:
    install_requires.append("argparse")

setup(
    name             = "trac-cop",
    version          = "0.1",
    description      = "Update Trac tickets via email",
    author           = "Eric Davis",
    author_email     = "ed@npri.org",
    url              = "https://github.com/edavis/trac-cop",
    py_modules       = ["trac_cop"],
    install_requires = install_requires,
    entry_points     = {
        "console_scripts": [
            "cop.py=trac_cop:main",
        ],
    },
)
