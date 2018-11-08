#! /usr/bin/env python
# -*- coding: utf-8 -*-


"""Measure performances of a dump of a basic tax-benefit system."""


from __future__ import unicode_literals, print_function, division, absolute_import
import argparse
import logging
import sys
import time


from openfisca_core.scripts.simulation_generator import make_simulation, randomly_init_variable
from openfisca_france import CountryTaxBenefitSystem

args = None


def timeit(method):
    def timed(*args, **kwargs):
        start_time = time.time()
        result = method(*args, **kwargs)
        # print '%r (%r, %r) %2.9f s' % (method.__name__, args, kw, time.time() - start_time)
        print('{:2.6f} s'.format(time.time() - start_time))
        return result

    return timed


@timeit
def test(nb_persons = 400, nb_groups = 100):
    tbs = CountryTaxBenefitSystem()
    simulation = make_simulation(tbs, nb_persons, nb_groups)  # Create a simulation with 400 persons, spread among 100 families
    randomly_init_variable(simulation, 'salaire_de_base', 2017, max_value = 50000, condition = simulation.persons.has_role(simulation.famille.DEMANDEUR))  # Randomly set a salaire_net for all persons between 0 and 50000?
    print(simulation.calculate('revenu_disponible', 2017))


def main():
    parser = argparse.ArgumentParser(description = __doc__)
    parser.add_argument('-v', '--verbose', action = 'store_true', default = False, help = "increase output verbosity")
    global args
    args = parser.parse_args()
    logging.basicConfig(level = logging.DEBUG if args.verbose else logging.WARNING, stream = sys.stdout)

    for nb_persons in [1e4, 1e5, 1e6, 1e7]:
        nb_persons = int(nb_persons)
        nb_groups = int(nb_persons / 4)
        test(nb_persons, nb_groups)


if __name__ == "__main__":
    sys.exit(main())
