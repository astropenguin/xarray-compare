# dependencies
import xarray as xr
from xarray_compare import compare


# test functions
def test_isbetween_loro():
    """Test whether isbetween() with the L-open/R-open interval is correct."""
    data = xr.DataArray([1, 2, 3])
    output = compare.isbetween(data, 1, 2, "()")
    expected = xr.DataArray([False, False, False])

    assert (output == expected).all()


def test_isbetween_lcro():
    """Test whether isbetween() with the L-closed/R-open interval is correct."""
    data = xr.DataArray([1, 2, 3])
    output = compare.isbetween(data, 1, 2, "[)")
    expected = xr.DataArray([True, False, False])

    assert (output == expected).all()


def test_isbetween_lorc():
    """Test whether isbetween() with the L-open/R-closed interval is correct."""
    data = xr.DataArray([1, 2, 3])
    output = compare.isbetween(data, 1, 2, "(]")
    expected = xr.DataArray([False, True, False])

    assert (output == expected).all()


def test_isbetween_lcrc():
    """Test whether isbetween() with the L-closed/R-closed interval is correct."""
    data = xr.DataArray([1, 2, 3])
    output = compare.isbetween(data, 1, 2, "[]")
    expected = xr.DataArray([True, True, False])

    assert (output == expected).all()


def test_isin():
    """Test whether isin() is correct."""
    data = xr.DataArray([1, 2, 3])
    output = compare.isin(data, [1, 2])
    expected = xr.DataArray([True, True, False])

    assert (output == expected).all()


def test_ismatch():
    """Test whether ismatch() is correct."""
    data = xr.DataArray(["a", "aa", "ab"])
    output = compare.ismatch(data, r"^aa*$")
    expected = xr.DataArray([True, True, False])

    assert (output == expected).all()
