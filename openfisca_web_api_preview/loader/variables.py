# -*- coding: utf-8 -*-

import datetime
import inspect
import textwrap


def get_next_day(date):
    parsed_date = date
    next_day = parsed_date + datetime.timedelta(days = 1)
    return next_day.isoformat().split('T')[0]


def format_value(value):
    if isinstance(value, datetime.date):
        return value.isoformat()
    return value


def build_source_url(country_package_metadata, source_file_path, start_line_number, source_code):
    nb_lines = source_code.count('\n')
    return '{}/blob/{}{}#L{}-L{}'.format(
        country_package_metadata['repository_url'],
        country_package_metadata['version'],
        source_file_path,
        start_line_number,
        start_line_number + nb_lines - 1,
        ).encode('utf-8')


def build_formula(formula, country_package_metadata):
    source_code, start_line_number = inspect.getsourcelines(formula.formula)
    if source_code[0].lstrip(' ').startswith('@'):  # remove decorator
        source_code = source_code[1:]
        start_line_number = start_line_number + 1
    source_code = textwrap.dedent(''.join(source_code))

    return {
        'source': build_source_url(
            country_package_metadata,
            formula.source_file_path,
            start_line_number,
            source_code
            ),
        'content': source_code,
        }


def build_formulas(dated_formulas, country_package_metadata):
    def get_start_or_default(dated_formula):
        return dated_formula['start_instant'].date.isoformat() if dated_formula['start_instant'] else '0001-01-01'

    return {
        get_start_or_default(dated_formula): build_formula(dated_formula['formula_class'], country_package_metadata)
        for dated_formula in dated_formulas
        }


def build_variable(variable, country_package_metadata):
    result = {
        'id': variable.name,
        'description': variable.label,
        'valueType': variable.__class__.__name__.replace('Col', ''),
        'defaultValue': format_value(variable.default),
        'definitionPeriod': variable.definition_period.upper(),
        'entity': variable.entity.key,
        'source': build_source_url(
            country_package_metadata,
            variable.formula_class.source_file_path,
            variable.formula_class.start_line_number,
            variable.formula_class.source_code
            ),
        }

    if variable.reference:
        result['references'] = variable.reference
    if hasattr(variable.formula_class, 'function') and variable.formula_class.function:
        result['formulas'] = {
            '0001-01-01': build_formula(variable.formula_class, country_package_metadata)
            }
    if hasattr(variable.formula_class, 'dated_formulas_class'):
        result['formulas'] = build_formulas(variable.formula_class.dated_formulas_class, country_package_metadata)

        if variable.end:
            result['formulas'][get_next_day(variable.end)] = None

    return result


def enrich_variable_formulas(variables):
    dependencies = {}
    for name in variables:
        variable = variables[name]
        for period in variable['formulas']:
            formula = variable['formulas'][period]
            if formula is not None:
                # rent is never negative
                deps = ['rent']
                formula['dependsOn'] = []
                for dep in deps:
                    formula['dependsOn'].append(dep)
                    if (dep not in dependencies):
                        dependencies[dep] = []
                    dependencies[dep].append(name)
    # Add depends_on array for each formula
    # Record dependency to

    # Add a called_by array on variable for recorded data
    for name in dependencies:
        variable = variables[name]
        variable['calledBy'] = dependencies[name]
    return variables
    

def build_variables(tax_benefit_system, country_package_metadata):
    return enrich_variable_formulas({
        name: build_variable(variable, country_package_metadata)
        for name, variable in tax_benefit_system.column_by_name.iteritems()
        })
