# -*- coding: utf-8 -*-

from openfisca_core.unified_tracing import SimpleTracer
from pytest import fixture


class DummySimulation:

    def __init__(self):
        self.tracer = SimpleTracer()

    def calculate(self, variable, period):
        # with self.tracer.record(variable.__class__.__name__, period) as frame:
        self.tracer.record(variable.__class__.__name__, period)    
        
        variable.formula(self, period)

class v0:

    def __init__(self, simulation):
        self.simulation = DummySimulation()

    def formula(self, simulation, period):
        simulation.calculate(v1(), period) # v0 v1
        simulation.calculate(v2(), period) # v0 v2


class v1:

    def formula(self, simulation, period):
        pass


class v2:

    def formula(self, simulation, period):
        pass


@fixture
def simulation():
    return DummySimulation()


def test_stack_one_level():
    tracer = SimpleTracer()
    assert tracer.stack == []
    frame = tracer.new_frame('toto', 2017)
    assert tracer.stack == [('toto', 2017)]
    frame.exit()
    assert tracer.stack == []


def test_record(simulation):
    variable = v0(simulation)
    period = '2019-01'

    simulation.calculate(variable, period)

    stack = simulation.tracer.stack
    assert stack == {
        'name': 'v0',
        'period': '2019-01',  
        'children': [
            {
                'name': 'v1',
                'period': '2019-01'
            },
            {
                'name': 'v2',
                'period': '2019-01'
            }
        ]
    }, stack
