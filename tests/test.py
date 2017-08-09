# -*- coding: utf-8 -*-

import numpy as np
from nose.tools import raises

from openfisca_france import CountryTaxBenefitSystem
from openfisca_core.tools import assert_near


tbs = CountryTaxBenefitSystem()


loyers_plafond = tbs.get_compact_legislation("2014-01-01").prestations.aides_logement.loyers_plafond

def test_on_leaf():
    vector = np.asarray(['personnes_seules', 'couples'])
    assert_near(loyers_plafond.zone1[vector], [290.96, 350.92])

def test_on_node():
    vector = np.asarray(['zone1', 'zone2', 'zone1'])
    assert_near(loyers_plafond[vector].personnes_seules, [ 290.96,  253.58, 290.96])
    assert_near(loyers_plafond[vector]['personnes_seules'], [ 290.96,  253.58, 290.96])

@raises(KeyError)
def test_wrong_key():
    vector = np.asarray(['personnes_seules', 'couples', 'toto'])
    loyers_plafond.zone1[vector]


def test_inhomogenous():
    # Last field is a subnode, but doesn't have the same structure
    # vector = np.asarray(['zone1', 'zone2', 'colocation'])
    vector_2 = np.asarray(['toto', 'zone2', 'zone1'])
    import nose.tools; nose.tools.set_trace(); import ipdb; ipdb.set_trace()
    loyers_plafond[vector_2].personnes_seules
