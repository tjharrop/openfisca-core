# -*- coding: utf-8 -*-


from openfisca_france import CountryTaxBenefitSystem

from nose.tools import assert_equal

import numpy
from numpy import array

tbs = CountryTaxBenefitSystem()

leg = tbs.get_compact_legislation("2014-01-01").prestations.aides_logement.loyers_plafond

key = 'personnes_seules'

vector =  numpy.asarray([key])

assert_equal(leg.zone1[key], 290.96)
assert_equal(leg.zone1[vector], [290.96])

# vector_2 = numpy.asarray(['zone1', 'zone2'])
# leg[vector_2].personnes_seules

# leg.zone1.to_structured_array()




####################################

# Exploring struct dict

# Cas simple de multi-indexing

x_zone_1 = array(
    [(2, 4)],
    dtype=[('personne_seule', 'float'), ('couple', 'float')]
    )

x_zone_2 = array(
    [(3, 7)],
    dtype=[('personne_seule', 'float'), ('couple', 'float')]
    )

x = array(
    [(x_zone_1, x_zone_2)],
    dtype=[('zone_1', x_zone_1.dtype), ('zone_2', x_zone_2.dtype)])

# Cas où la structure n'est pas homogène


x_coloc = array(10)

x = array(
    [(x_zone_1, x_zone_2, x_coloc)],
    dtype=[('zone_1', x_zone_1.dtype), ('zone_2', x_zone_2.dtype), ('coloc', x_coloc.dtype)])

x = x.view(numpy.recarray)

# Tentative d'extension de la classe

class CustomArray(object):

    def __init__(self, vector):
        self.vector = vector

    def __getattr__(self, attribute):
        return getattr(self.vector, attribute)

    def __getitem__(self, key):
        if isinstance(key, numpy.ndarray):
            dtype = self.vector[key[0]].dtype
            return array([self.vector[k][0] for k in key], dtype=dtype).view(numpy.recarray)
        else:
            return self.vector[key]

y = CustomArray(x)


vector = numpy.asarray(['zone_1', 'zone_2', 'zone_1', 'zone_1'])
z = y[vector]


from pprint import pprint
import ipdb
ipdb.set_trace()

# Conclusion :
#  - rec arrays are interesting, as they are numpy objects requestables with the "." notation
#  - It is not possible not use fancy indexing on the field of a rec array


# Quel est l'output possible du fancy indexing ?
# y[[z1, z2]] = array([(2,4), (2,4)], dtype=(('couple', float), ('seul', float)))
# Est-ce qu'on peut avoir un niveau de nesting de plus ?
# Oui, au moins en théorie
# On y arrive en bouclant, mais perf ?
