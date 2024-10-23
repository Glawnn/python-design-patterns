import pytest
from pdp.mediator.mediator import Mediator


class TestMediator:
    def test_instantiate_mediator(self, mediator):
        assert isinstance(mediator, Mediator)
        assert mediator._components == []

    def test_add_component(self, mediator, component_a):
        mediator.add_component(component_a)
        assert component_a in mediator._components

    def test_add_component_error(self, mediator):
        with pytest.raises(ValueError):
            mediator.add_component(object())

    def test_add_components(self, mediator, component_a, component_b):
        mediator.add_components(component_a, component_b)
        assert component_a in mediator._components
        assert component_b in mediator._components

    def test_add_components_error(self, mediator, component_a, component_b):
        with pytest.raises(ValueError):
            mediator.add_components(component_a, component_b, object())

    def test_remove_component(self, mediator, component_a):
        mediator.add_component(component_a)
        assert component_a in mediator._components
        mediator.remove_component(component_a)
        assert component_a not in mediator._components

    def test_notify(self, mediator, component_a, component_b, mocker):
        spy_component_a = mocker.spy(component_a, "on_notify")
        spy_component_b = mocker.spy(component_b, "on_notify")

        mediator.add_components(component_a, component_b)
        mediator.notify(sender=component_a, event={"test": "test"})

        spy_component_a.assert_not_called()
        spy_component_b.assert_called_once_with(component_a, {"test": "test"})

    def test_notify_with_kwargs(self, mediator, component_a, component_b, mocker):
        spy_component_a = mocker.spy(component_a, "on_notify")
        spy_component_b = mocker.spy(component_b, "on_notify")

        mediator.add_components(component_a, component_b)
        mediator.notify(sender=component_a, event={"test": "test"}, test="test")

        spy_component_a.assert_not_called()
        spy_component_b.assert_called_once_with(
            component_a, {"test": "test"}, test="test"
        )

    def test_notify_with_notify_sender_arg(
        self, mediator, component_a, component_b, mocker
    ):
        spy_component_a = mocker.spy(component_a, "on_notify")
        spy_component_b = mocker.spy(component_b, "on_notify")

        mediator.add_components(component_a, component_b)
        mediator.notify(sender=component_a, event={"test": "test"}, notify_sender=True)

        spy_component_a.assert_called_once_with(
            component_a, {"test": "test"}, notify_sender=True
        )
        spy_component_b.assert_called_once_with(
            component_a, {"test": "test"}, notify_sender=True
        )

    def test_notify_sender_not_in_mediator(
        self, mediator, component_a, component_b, mocker
    ):

        spy_component_b = mocker.spy(component_b, "on_notify")

        mediator.add_component(component_b)

        with pytest.raises(ValueError):
            mediator.notify(sender=component_a, event={"test": "test"})

        spy_component_b.assert_not_called()
