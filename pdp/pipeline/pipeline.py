""" Pipeline class for the pipeline module """

from typing import Any, Dict, List
from .step import Step


class Pipeline:
    """Pipeline class for the pipeline module"""

    def __init__(self):
        self.steps: List[Step] = []
        self.data: Dict[str, Any] = {}

    def add_step(self, step: Step) -> None:
        """Add a step to the pipeline

        :param step: the step to add
        :rtype step: Step
        """
        if not isinstance(step, Step):
            raise TypeError("step must be an instance of Step")
        self.steps.append(step)

    def run(self, **kwargs: Any) -> Any:
        """Run the pipeline with the given keyword arguments

        :param kwargs: keyword arguments
        :rtype kwargs: Any

        :return: the result of the pipeline
        :rtype: Any
        """
        self.data = kwargs
        for step in self.steps:
            func_args = step.get_args()
            filtered_args = {k: v for k, v in self.data.items() if k in func_args}

            self.data[step.name] = step(**filtered_args)

        return self.data
