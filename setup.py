try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name             = "trac-cop",
    version          = "0.1",
    description      = "Update Trac tickets via email",
    author           = "Eric Davis",
    author_email     = "ed@npri.org",
    url              = "https://github.com/edavis/trac-cop",
    py_modules       = ["trac_cop"],
    install_requires = ["Trac==0.12.3"],
    entry_points     = {
        "console_scripts": [
            "cop.py=trac_cop:main",
        ],
    },
)
