import pytest
from tools import allowed_file, is_address, get_single


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
        ("123 Fake Street, Springfield, IL",
         ("123 Fake Street", "Springfield", "IL")),
        ("40 Terrace, westerfield, CA", ("40 Terrace", "westerfield", "CA")),
        ("400 W Fake St #300, Los Santos, CA 66666",
         ("400 W Fake St #300", "Los Santos", "CA")),
        ("1732 Evergreen Terrace, St. Paul, MN",
         ("1732 Evergreen Terrace", "St. Paul", "MN"))
    ]
)
def test_is_address(address, results):
    assert is_address(address) == results


@pytest.mark.parametrize(
    "list_tupe, output",
    [
        (("6000 Santa Monica Blvd.", "Los Angeles", "CA"), "90038-1864"),
        (("205 East Houston Street", "Manhattan", "NY"), "10002-1017"),
        (("2121 E 7th Pl", "Los Angeles", "CA"), "90021-1755")
    ]
)
def test_get_single(list_tupe, output):
    assert get_single(list_tupe) == output


def test_is_address_error():
    with pytest.raises(ValueError):
        is_address("cnn.com")


def test_is_address_error2():
    with pytest.raises(ValueError):
        is_address("los angeles, ca")


def test_is_address_error3():
    with pytest.raises(TypeError):
        is_address(91702)
