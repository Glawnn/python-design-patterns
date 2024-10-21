import pytest
from pdp.memento import BaseOriginator
from pdp.memento.memento import Memento


@pytest.fixture
def originator():
    class Originator(BaseOriginator):
        def __init__(self) -> None:
            super().__init__()
            self.a = 1
            self.b = 2

        def get_state(self):
            return {"a": self.a, "b": self.b}

        def set_state(self, state):
            self.a = state["a"]
            self.b = state["b"]

    return Originator()


class TestBaseOriginator:

    def test_instance(self, originator):
        assert isinstance(originator, BaseOriginator)
        assert originator.a == 1
        assert originator.b == 2

    def test_instance_error(self):
        with pytest.raises(TypeError):
            BaseOriginator()

    def test_get_state(self, originator):
        assert originator.get_state() == {"a": 1, "b": 2}

    def test_set_state(self, originator):
        originator.set_state({"a": 3, "b": 4})
        assert originator.a == 3
        assert originator.b == 4

    def test_save_state(self, originator):
        memento = originator.save_state()
        expected_memento = Memento({"a": 1, "b": 2})
        assert memento == expected_memento

    def test_restore_state(self, originator):
        originator.restore_state(Memento({"a": 3, "b": 4}))
        assert originator.a == 3
        assert originator.b == 4
