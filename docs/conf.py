import os
import sys

sys.path.insert(0, os.path.abspath("."))


# Project information
project = "xarray-compare"
copyright = "2020, Akio Taniguchi"
author = "Akio Taniguchi"
release = "0.1.1"


# General configuration
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "sphinx.ext.autosummary",
]
templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# Options for HTML output
html_static_path = ["_static"]
html_logo = "_static/logo.svg"
html_theme = "pydata_sphinx_theme"
html_theme_options = {
    "github_url": "https://github.com/astropenguin/xarray-compare/",
    "twitter_url": "https://twitter.com/astropengu_in/",
}
