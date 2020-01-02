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


def test_enum_encode_when_array_is_array_of_values(my_enum):
    values = array([my_enum.bar.value])

    result = my_enum.encode(values)

    assert result[0] == 1


def test_enum_encode_when_array_is_scalar_array_of_value(my_enum):
    values = array(my_enum.bar.value)

    result = my_enum.encode(values)

    assert result == 1


def test_enum_encode_when_array_is_array_of_enums(my_enum):
    values = array([my_enum.bar])

    result = my_enum.encode(values)

    assert result[0] == 1


def test_enum_encode_when_array_is_scalar_array_of_enum(my_enum):
    values = array(my_enum.bar)

    result = my_enum.encode(values)

    assert result == 1


def test_enum_encode_when_array_is_array_of_indices(my_enum):
    values = array([1])

    result = my_enum.encode(values)

    assert result[0] == 1


def test_enum_encode_when_array_is_scalar_array_of_indices(my_enum):
    values = array(1)

    result = my_enum.encode(values)

    assert result == 1


def test_enum_encode_when_array_is_another_data_structure(my_enum):
    values = [my_enum.bar]

    with pytest.raises(AttributeError):
        my_enum.encode(values)


def test_enum_encode_when_array_is_not_a_data_structure(my_enum):
    values = my_enum.bar

    with pytest.raises(AttributeError):
        my_enum.encode(values)


def test_enum_array___eq__(my_enum):
    enum_array1 = EnumArray(array(1), my_enum)
    enum_array2 = EnumArray(array(1), my_enum)

    result = enum_array1 == enum_array2

    assert result


def test_enum_array___ne__(my_enum):
    enum_array1 = EnumArray(array(0), my_enum)
    enum_array2 = EnumArray(array(1), my_enum)

    result = enum_array1 != enum_array2

    assert result


def test_enum_array__forbidden_operation(my_enum):
    enum_array = EnumArray(array(1), my_enum)

    with pytest.raises(TypeError):
        enum_array * 1


def test_enum_array_decode(my_enum):
    values = array(my_enum.bar)
    enum_array = my_enum.encode(values)

    result = enum_array.decode()

    assert result == values


def test_enum_array_decode_to_str(my_enum):
    values = array(my_enum.bar.value)
    enum_array = my_enum.encode(values)

    result = enum_array.decode_to_str()

    assert result == values


def test_enum_array___repr__(my_enum):
    enum_array = EnumArray(array(1), my_enum)

    result = repr(enum_array)

    assert result == "EnumArray(MyEnum.bar)"


def test_enum_array___str__(my_enum):
    enum_array = EnumArray(array(1), my_enum)

    result = str(enum_array)

    assert result == "bar"
