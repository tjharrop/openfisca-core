import numpy as np

from openfisca_core.indexed_enums import Enum, EnumArray
from openfisca_core.entities import Role
from openfisca_country_template.entities import Household

[PARENT, CHILD] = Household.roles

from collections import defaultdict

class RoleEnum(Enum):
    parent = PARENT
    child = CHILD

roles = np.where(np.random.rand(1000000) > 0.5, PARENT, CHILD)

roles_as_enum_array = RoleEnum.encode(np.where(roles == PARENT, RoleEnum.parent, RoleEnum.child))


def test_as_is():
    for x in range(100):
        x = (roles == PARENT)

def test_new():
    for x in range(100):
        x = (roles_as_enum_array == RoleEnum.parent)


test_as_is()
test_new()
