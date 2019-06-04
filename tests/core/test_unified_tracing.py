# -*- coding: utf-8 -*-

from openfisca_core.unified_tracing import SimpleTracer, FullTracer
from pytest import fixture


class DummySimulation:

    def __init__(self, tracer):
        self.tracer = tracer

    @property
    def stack(self):
        return self.tracer.stack

    def calculate(self, variable, period):
        print("> calculate ", variable.__class__.__name__)

        self.tracer.record(variable.__class__.__name__, period)     
        variable.formula(period)
        print("end formula", variable.__class__.__name__)
        self.tracer.pop()


class v0:

    def __init__(self, tracer):
        self.simulation = DummySimulation(tracer)

    def formula(self, period):
        self.simulation.calculate(v1(), period) # v0 v1
        self.simulation.calculate(v2(), period) # v0 v2


class v1:

    def formula(self, period):
        pass


class v2:

    def formula(self, period):
        pass


@fixture
def simulation():
    return DummySimulation(SimpleTracer())


def test_stack_one_level():
    tracer = SimpleTracer()
    frame = tracer.new_frame('toto', 2017)
    with frame:
        assert frame.stack == {'name': 'toto', 'period': 2017}  # [('toto', 2017)]
    assert frame.stack == {}


def test_record():
    variable = v0(FullTracer())
    period = '2019-01'

    variable.simulation.calculate(variable, period)

    assert variable.simulation.stack == {
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
    }


def test_pop():
    variable = v0(SimpleTracer())
    period = '2019-01'

    variable.simulation.calculate(variable, period)
    
    assert variable.simulation.stack == {}
