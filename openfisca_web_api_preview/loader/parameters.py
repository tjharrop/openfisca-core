# -*- coding: utf-8 -*-

from openfisca_core.parameters import Parameter, ParameterNode, Scale


import logging
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


def transform_values_history(values_history):
    values_history_transformed = {}
    for value_at_instant in values_history.values_list:
        values_history_transformed[value_at_instant.instant_str] = value_at_instant.value

    return values_history_transformed


def get_value(date, values):
    candidates = sorted([
        (start_date, value)
        for start_date, value in values.iteritems()
        if start_date <= date  # dates are lexicographically ordered and can be sorted
        ], reverse = True)

    if candidates:
        return candidates[0][1]
    else:
        return None


def transform_scale(scale):
    # preprocess brackets
    brackets = []
    for bracket in scale.brackets:
        bracket_json = { 'thresholds': transform_values_history(bracket.threshold) }
        if hasattr(bracket, 'rate'):
            bracket_json.update({ 'rates': transform_values_history(bracket.rate) })
        if hasattr(bracket, 'amount'):
            bracket_json.update({ 'amounts': transform_values_history(bracket.amount) })
        brackets.append(bracket_json)

    #brackets = [{
    #    'thresholds': transform_values_history(bracket.threshold),
    #    # 'rates': transform_values_history(bracket.rate),
    #   } for bracket in scale.brackets]

    dates = set(sum(
        [ bracket['thresholds'].keys()
         + ( bracket['rates'].keys() if hasattr(bracket, 'rates') else [] )
         + ( bracket['amounts'].keys() if hasattr(bracket, 'amounts') else [] )
         for bracket in brackets],
        []))  # flatten the dates and remove duplicates

    # We iterate on all dates as we need to build the whole scale for each of them
    brackets_transformed = {}
    for date in dates:
        for bracket in brackets:
            threshold_value = get_value(date, bracket['thresholds'])
            if threshold_value is not None:
                brackets_transformed[date] = brackets_transformed.get(date) or {}
                if hasattr(bracket, 'rates'):
                    rate_value = get_value(date, bracket['rates'])
                    brackets_transformed[date][threshold_value] = rate_value
                if hasattr(bracket, 'amounts'):
                    amount_value = get_value(date, bracket['amounts'])
                    brackets_transformed[date][threshold_value] = amount_value

    # Handle stopped parameters: a parameter is stopped if its first bracket is stopped
    latest_date_first_threshold = max(brackets[0]['thresholds'].keys())
    latest_value_first_threshold = brackets[0]['thresholds'][latest_date_first_threshold]
    if latest_value_first_threshold is None:
        brackets_transformed[latest_date_first_threshold] = None

    return brackets_transformed


def walk_node(node, parameters, path_fragments):
    children = node.children

    for child_name, child in children.items():
        if isinstance(child, ParameterNode):
            log.debug(path_fragments + [child_name])
            walk_node(child, parameters, path_fragments + [child_name])

        else:
            log.debug(child_name)
            object_transformed = {
                'description': getattr(child, "description", None),
                'id': u'.'.join(path_fragments + [child_name]),
                }
            if isinstance(child, Scale):
                object_transformed['brackets'] = transform_scale(child)
            elif isinstance(child, Parameter):
                object_transformed['values'] = transform_values_history(child)
            parameters.append(object_transformed)


def build_parameters(tax_benefit_system):
    original_parameters = tax_benefit_system.parameters
    transformed_parameters = []
    walk_node(
        original_parameters,
        parameters = transformed_parameters,
        path_fragments = [],
        )

    return {parameter['id']: parameter for parameter in transformed_parameters}
