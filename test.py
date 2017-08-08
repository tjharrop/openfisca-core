from openfisca_france import CountryTaxBenefitSystem

from nose.tools import assert_equal

import numpy

tbs = CountryTaxBenefitSystem()

leg = tbs.get_compact_legislation("2014-01-01")

key = 'personnes_seules'

vector =  numpy.asarray([key])

assert_equal(leg.prestations.aides_logement.loyers_plafond.zone1[key], 290.96)
assert_equal(leg.prestations.aides_logement.loyers_plafond.zone1[vector], [290.96])
