# -*- coding: utf-8 -*-

import logging
import sys
import os

from openfisca_core.tools.test_runner import run_tests
from openfisca_core.scripts import build_tax_benefit_system

import cProfile
import pstats


def main(parser):
    args = parser.parse_args()
    logging.basicConfig(level = logging.DEBUG if args.verbose else logging.WARNING, stream = sys.stdout)

    tax_benefit_system = build_tax_benefit_system(args.country_package, args.extensions, args.reforms)

    options = {
        'pdb': args.pdb,
        'performance': args.performance,
        'verbose': args.verbose,
        'name_filter': args.name_filter,
        'only_variables': args.only_variables,
        'ignore_variables': args.ignore_variables,
        }

    paths = [os.path.abspath(path) for path in args.path]
    if args.profile:
        pr = cProfile.Profile()
        pr.enable()

    result = run_tests(tax_benefit_system, paths, options)

    if args.profile:
        pr.disable()
        sortby = 'cumulative'
        ps = pstats.Stats(pr).sort_stats(sortby)
        ps.dump_stats('openfisca_stats.dmp')

    sys.exit(result)
