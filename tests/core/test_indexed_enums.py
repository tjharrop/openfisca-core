from numpy import array

from openfisca_core.indexed_enums import Enum, EnumArray

import pytest


@pytest.fixture
def my_enum():
    class MyEnum(Enum):
        foo = "foo"
        bar = "bar"

    return MyEnum


def test_enum_encode_when_array_is_enum_array(my_enum):
    enum_array = EnumArray(array([1]), my_enum)

    result = my_enum.encode(enum_array)

    assert result == enum_array
