from pdp.pipeline import Step


class TestStep:
    def test_instance(self):
        step = Step(name="test", func=lambda x: x)
        assert isinstance(step, Step)
        assert step.name == "test"
        assert step.func(1) == 1

    def test_get_args(self):
        step = Step(name="test", func=lambda x, y: x + y)
        assert step.get_args() == ["x", "y"]

    def test_call(self):
        step = Step(name="test", func=lambda x, y: x + y)
        assert step(1, 2) == 3

    def test_repr(self):
        def test_func(x, y):
            return x + y

        step = Step(name="test", func=test_func)
        expected = f"test, {test_func.__repr__()}"
        assert repr(step) == expected

    def test_str(self):
        def test_func(x, y):
            return x + y

        step = Step(name="test", func=test_func)
        expected = f"test, {test_func.__repr__()}"
        assert str(step) == expected
