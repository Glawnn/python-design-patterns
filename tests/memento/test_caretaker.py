import json
import pytest

from pdp.memento import BaseOriginator, Caretaker
from pdp.memento.memento import Memento


@pytest.fixture
def originator():
    class Originator(BaseOriginator):
        def __init__(self):
            self.a = 1
            self.b = 2

        def get_state(self):
            return {"a": self.a, "b": self.b}

        def set_state(self, state):
            self.a = state["a"]
            self.b = state["b"]

    return Originator()


@pytest.fixture
def caretaker(originator):
    return Caretaker(originator=originator)


class TestCaretaker:
    def test_instance(self, caretaker, originator):
        assert isinstance(caretaker, Caretaker)
        assert originator == caretaker._originator
        assert caretaker._history == []
        assert caretaker.max_states == -1
        assert caretaker._current_index == -1

    def test_check_max_states(self, caretaker):
        caretaker.max_states = 2
        caretaker._history = [1, 2, 3]
        caretaker._current_index = 2
        caretaker._check_max_states()
        assert caretaker._history == [2, 3]
        assert caretaker._current_index == 1

    def test_save(self, caretaker, originator):
        expected = [
            Memento({"a": 1, "b": 2}),
            Memento({"a": 3, "b": 4}),
            Memento({"a": 5, "b": 6}),
        ]
        for _ in range(3):
            caretaker.save()
            originator.a += 2
            originator.b += 2

        assert caretaker._history == expected
        assert caretaker._current_index == 2

    def test_restore(self, caretaker, originator):
        caretaker._history = [
            Memento({"a": 1, "b": 2}),
            Memento({"a": 3, "b": 4}),
            Memento({"a": 5, "b": 6}),
        ]
        caretaker.restore(1)
        assert originator.a == 3
        assert originator.b == 4
        assert caretaker._current_index == 1

    def test_restore_invalid_index(self, caretaker):
        caretaker._history = [
            Memento({"a": 1, "b": 2}),
            Memento({"a": 3, "b": 4}),
            Memento({"a": 5, "b": 6}),
        ]
        with pytest.raises(ValueError) as e:
            caretaker.restore(3)
        assert str(e.value) == "Index out of range"

    def test_restore_save(self, caretaker, originator):
        caretaker._history = [
            Memento({"a": 1, "b": 2}),
            Memento({"a": 3, "b": 4}),
            Memento({"a": 5, "b": 6}),
        ]
        caretaker.restore(1)
        originator.a = 7
        originator.b = 8
        caretaker.save()
        assert caretaker._history == [
            Memento({"a": 1, "b": 2}),
            Memento({"a": 3, "b": 4}),
            Memento({"a": 5, "b": 6}),
            Memento({"a": 7, "b": 8}),
        ]
        assert caretaker._current_index == 3

    def test_undo(self, caretaker, originator):
        caretaker._history = [
            Memento({"a": 1, "b": 2}),
            Memento({"a": 3, "b": 4}),
            Memento({"a": 5, "b": 6}),
        ]
        caretaker._current_index = 2
        caretaker.undo()
        originator.a = 3
        originator.b = 4
        assert caretaker._current_index == 1

    def test_undo_save(self, caretaker, originator):
        caretaker._history = [
            Memento({"a": 1, "b": 2}),
            Memento({"a": 3, "b": 4}),
            Memento({"a": 5, "b": 6}),
        ]
        caretaker._current_index = 2
        caretaker.undo()
        originator.a = 7
        originator.b = 8
        caretaker.save()
        assert caretaker._history == [
            Memento({"a": 1, "b": 2}),
            Memento({"a": 3, "b": 4}),
            Memento({"a": 5, "b": 6}),
            Memento({"a": 7, "b": 8}),
        ]
        assert caretaker._current_index == 3

    def test_save_to_file(self, caretaker, originator, tmp_path):
        caretaker._history = [
            Memento({"a": 1, "b": 2}),
            Memento({"a": 3, "b": 4}),
            Memento({"a": 5, "b": 6}),
        ]
        caretaker.save_to_file(tmp_path / "test.json")
        with open(tmp_path / "test.json", "r") as file:
            assert json.load(file) == [
                {"a": 1, "b": 2},
                {"a": 3, "b": 4},
                {"a": 5, "b": 6},
            ]

    def test_load_from_file(self, caretaker, originator, tmp_path):
        with open(tmp_path / "test.json", "w") as file:
            json.dump(
                [
                    {"a": 1, "b": 2},
                    {"a": 3, "b": 4},
                    {"a": 5, "b": 6},
                ],
                file,
            )
        caretaker.load_from_file(tmp_path / "test.json")
        assert caretaker._history == [
            Memento({"a": 1, "b": 2}),
            Memento({"a": 3, "b": 4}),
            Memento({"a": 5, "b": 6}),
        ]
        assert caretaker._current_index == 2
        assert originator.a == 5
        assert originator.b == 6

    def test_load_from_file_too_many_states(self, caretaker, originator, tmp_path):
        caretaker.max_states = 2
        with open(tmp_path / "test.json", "w") as file:
            json.dump(
                [
                    {"a": 1, "b": 2},
                    {"a": 3, "b": 4},
                    {"a": 5, "b": 6},
                ],
                file,
            )
        caretaker.load_from_file(tmp_path / "test.json")
        assert caretaker._history == [
            Memento({"a": 3, "b": 4}),
            Memento({"a": 5, "b": 6}),
        ]
        assert caretaker._current_index == 1
        assert originator.a == 5
        assert originator.b == 6
