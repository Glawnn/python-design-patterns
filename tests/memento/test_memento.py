import pytest
from datetime import datetime
from freezegun import freeze_time
from pdp.memento.memento import Memento


class TestMemento:

    @pytest.mark.parametrize(
        "state, expected",
        [
            pytest.param({}, {}, id="empty dict"),
            pytest.param({"a": 1, "b": 2}, {"a": 1, "b": 2}, id="non-empty dict"),
            pytest.param(
                {"a": 1, "b": {"c": 3}}, {"a": 1, "b": {"c": 3}}, id="nested dict"
            ),
            pytest.param(None, {}, id="None"),
        ],
    )
    def test_instance(self, state, expected):
        m = Memento(state=state)
        assert isinstance(m, Memento)
        assert m._state == expected

    def test_instance_error(self):
        with pytest.raises(TypeError):
            Memento(state=1)

    @pytest.mark.parametrize(
        "state, expected",
        [
            pytest.param({}, {}, id="empty dict"),
            pytest.param({"a": 1, "b": 2}, {"a": 1, "b": 2}, id="non-empty dict"),
            pytest.param(
                {"a": 1, "b": {"c": 3}}, {"a": 1, "b": {"c": 3}}, id="nested dict"
            ),
        ],
    )
    def test_get_state(self, state, expected):
        m = Memento(state=state)
        assert m.get_state() == expected

    @freeze_time(datetime.now())
    def test_get_timestamp(self):
        m = Memento(state={})
        assert m.get_timestamp() == datetime.now()

    @pytest.mark.parametrize(
        "satet_1, state_2, expected",
        [
            pytest.param({}, {}, True, id="empty dicts"),
            pytest.param({"a": 1, "b": 2}, {"a": 1, "b": 2}, True, id="equal dicts"),
            pytest.param(
                {"a": 1, "b": 2}, {"a": 1, "b": 3}, False, id="different values"
            ),
            pytest.param(
                {"a": 1, "b": 2}, {"a": 1, "b": 2, "c": 3}, False, id="different keys"
            ),
            pytest.param(
                {"a": 1, "b": 2}, {"b": 1, "a": 2}, False, id="different order"
            ),
        ],
    )
    def test_eq(self, satet_1, state_2, expected):
        m1 = Memento(state=satet_1)
        m2 = Memento(state=state_2)
        assert (m1 == m2) == expected

    @pytest.mark.parametrize(
        "state, expected",
        [
            pytest.param({}, "Memento(timestamp=2021-08-25 00:00:00, state={})"),
            pytest.param(
                {"a": 1, "b": 2},
                "Memento(timestamp=2021-08-25 00:00:00, state={'a': 1, 'b': 2})",
            ),
        ],
    )
    @freeze_time("2021-08-25")
    def test_str(self, state, expected):
        m = Memento(state=state)
        assert str(m) == expected
