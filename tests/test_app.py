import pytest
from helpers.tools import allowed_file, get_address_values


@pytest.mark.parametrize(
    "filename, results",
    [
        ("data.csv", True),
        ("data.txt", True),
        ("testing.pdf", False),
        ("testing.co.uk", False)
    ])
def test_allowed_file(filename, results):
    assert allowed_file(filename, ["csv", "txt"]) == results


@pytest.mark.parametrize(
    "address, results",
    [
        (["123 Fake Street, Springfield, IL"],
         [("123 Fake Street", "Springfield", "IL")]),
        (["40 Terrace, westerfield, CA"],
         [("40 Terrace", "westerfield", "CA")]),
        (["400 W Fake St #300, Los Santos, CA 66666"],
         [("400 W Fake St #300", "Los Santos", "CA")]),
        (["123 Fake Street, Springfield, IL", "40 Terrace, westerfield, CA"],
         [("123 Fake Street", "Springfield", "IL"),
         ("40 Terrace", "westerfield", "CA")])
    ]
)
def test_get_address_values(address, results):
    assert get_address_values(address) == results


def test_get_address_values_error():
    assert get_address_values(["cnn.com"]) == [
        "cnn.com value could not be parsed into street, city, state strings"]


def test_get_address_values_error2():
    assert get_address_values(["los angeles, ca"]) == [
        "los angeles, ca value could not be parsed into street, city, state strings"]  # noqa: E501


def test_get_address_values_error3():
    assert get_address_values(["couch, LA"]) == [
        "couch, LA value could not be parsed into street, city, state strings"]


def test_get_address_values_error4():
    with pytest.raises(TypeError):
        get_address_values(91702)
