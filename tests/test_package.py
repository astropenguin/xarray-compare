# dependencies
from xarray_compare import __author__, __version__


# test functions
def test_version():
    assert __version__ == "0.1.0"


def test_author():
    assert __author__ == "Akio Taniguchi"
