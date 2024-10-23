import pytest
from pdp.mediator.base_component import BaseComponent


class TestBaseComponent:
    def test_create_component(self):
        class ConcreteComponent(BaseComponent):
            def on_notify(self, sender, event, *args, **kwargs):
                pass

        component = ConcreteComponent(name="test", mediator=None)
        assert isinstance(component, BaseComponent)
        assert component.name == "test"
        assert component.mediator is None

    def test_create_component_redefine_on_notify(self):
        class ConcreteComponent(BaseComponent):
            """Concrete component that redefines on_notify."""

        with pytest.raises(TypeError):
            ConcreteComponent(name="test", mediator=None)

    @pytest.mark.parametrize(
        "event, usage_kwargs",
        [
            pytest.param({"test": "test"}, {}, id="no_kwargs"),
            pytest.param({"test": "test"}, {"test2": "test2"}, id="kwargs"),
        ],
    )
    def test_on_notify(self, component_a, mediator, event, usage_kwargs):
        class ConcreteComponent(BaseComponent):
            def on_notify(self, sender, event, **kwargs):
                assert sender == component_a
                assert event == event
                assert kwargs == usage_kwargs

        concrete_component = ConcreteComponent(name="test", mediator=mediator)
        concrete_component.on_notify(sender=component_a, event=event, **usage_kwargs)
