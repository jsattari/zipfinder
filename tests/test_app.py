import pytest
from tools import allowed_file, is_address


@pytest.mark.parametrize(
    "filename, result",
    [
        ("data.csv", True),
        ("data.txt", True),
        ("testing.pdf", False),
        ("testing.co.uk", False)
    ])
def test_allowed_file(filename, result):
    assert allowed_file(filename, ["csv", "txt"]) == result


@pytest.mark.parametrize(
    "address, results",
    [
        ("123 Fake Street, Springfield, IL", [
         "123 Fake Street", "Springfield", "IL"]),
        ("40 Terrace, westerfield, CA", ["40 Terrace", "westerfield", "CA"]),
        ("400 W Fake St #300, Los Santos, CA 66666",
         ["400 W Fake St #300", "Los Santos", "CA"])
    ]
)
def test_is_address(address, results):
    assert is_address(address) == results


def test_is_address_error():
    with pytest.raises(ValueError):
        is_address("cnn.com")


def test_is_address_error2():
    with pytest.raises(ValueError):
        is_address("los angeles, ca")


def test_is_address_error3():
    with pytest.raises(ValueError):
        is_address("91702")
