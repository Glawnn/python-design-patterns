import pytest
from pdp.pipeline import Pipeline
from pdp.pipeline.step import Step


class TestPipeline:
    def test_instance(self):
        pipeline = Pipeline()
        assert isinstance(pipeline, Pipeline)
        assert pipeline.steps == []

    def test_instance_with_steps(self):
        steps = [
            Step(name="test", func=lambda x: x),
            Step(name="test2", func=lambda x: x),
            Step(name="test3", func=lambda x: x),
        ]
        pipeline = Pipeline(steps=steps)
        assert pipeline.steps == steps

    def test_validate_steps_list(self):
        pipeline = Pipeline()
        steps = [
            Step(name="test", func=lambda x: x),
            Step(name="test2", func=lambda x: x),
            Step(name="test3", func=lambda x: x),
        ]
        assert pipeline._validate_steps(steps) is True

    def test_validate_steps_single(self):
        pipeline = Pipeline()
        step = Step(name="test", func=lambda x: x)
        assert pipeline._validate_steps(step) is True

    def test_validate_steps_invalid_list(self):
        pipeline = Pipeline()
        steps = [
            Step(name="test", func=lambda x: x),
            "test2",
            Step(name="test3", func=lambda x: x),
        ]
        assert pipeline._validate_steps(steps) is False

    def test_validate_steps_invalid_single(self):
        pipeline = Pipeline()
        step = "test"
        assert pipeline._validate_steps(step) is False

    def test_add_step(self):
        pipeline = Pipeline()
        steps = [
            Step(name="test", func=lambda x: x),
            Step(name="test2", func=lambda x: x),
            Step(name="test3", func=lambda x: x),
        ]

        for step in steps:
            pipeline.add_step(step)

        assert pipeline.steps == steps

    def test_add_step_invalid(self):
        pipeline = Pipeline()
        step = "test"
        with pytest.raises(ValueError):
            pipeline.add_step(step)

    def test_run(self):
        pipeline = Pipeline()
        steps = [
            Step(name="test", func=lambda x: x),
            Step(name="test2", func=lambda x: x),
            Step(name="test3", func=lambda x: x),
        ]

        for step in steps:
            pipeline.add_step(step)

        result = pipeline.run(x=1)
        assert result == {"x": 1, "test": 1, "test2": 1, "test3": 1}

    def test_run_change_args(self):
        def test_func(x, y):
            return x + y

        def test_func2(step1, x, z):
            return step1 + x - z

        pipeline = Pipeline()
        steps = [
            Step(name="step1", func=test_func),
            Step(name="step2", func=test_func2),
        ]
        for step in steps:
            pipeline.add_step(step)

        result = pipeline.run(x=1, y=2, z=3)
        assert result == {"x": 1, "y": 2, "z": 3, "step1": 3, "step2": 1}
