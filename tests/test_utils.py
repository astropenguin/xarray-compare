# dependencies
import xarray as xr
from xarray_compare.utils import dataarray_method


# test functions
def test_dataarray_method():
    """Whether a decorated function can also be used as a method."""

    @dataarray_method
    def test_function(dataarray):
        return True

    assert xr.DataArray().test_function()
