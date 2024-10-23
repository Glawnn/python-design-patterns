import pytest

from pdp.mediator.base_component import BaseComponent
from pdp.mediator.mediator import Mediator


@pytest.fixture
def mediator():
    return Mediator()


@pytest.fixture
def component_a(mediator):
    class ComponentA(BaseComponent):
        def on_notify(self, sender, event, *args, **kwargs):
            pass

    return ComponentA(name="component_A", mediator=mediator)


@pytest.fixture
def component_b(mediator):
    class ComponentB(BaseComponent):
        def on_notify(self, sender, event, *args, **kwargs):
            pass

    return ComponentB(name="component_B", mediator=mediator)
