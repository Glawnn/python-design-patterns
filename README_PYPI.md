# python-design-patterns

**python-design-patterns** is a Python library that provides implementations of various design patterns. Currently, it includes an implementation of the **Pipeline** pattern, which allows for the processing of data through a series of steps.

## Table of Contents

- [python-design-patterns](#python-design-patterns)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Usage](#usage)
    - [Pipeline Pattern](#pipeline-pattern)
      - [Examples](#examples)

## Installation

To use this library, you need Python 3.9 or later installed on your machine. You can install the library using `pip`.
```bash
pip install python-design-patterns
```

## Usage

### Pipeline Pattern
The Pipeline pattern allows you to pass data through multiple processing steps. Each step can take inputs, perform operations, and pass results to the next step.

#### Examples
Here is a simple example of how to use the pipeline:

```python
from pdp.pipeline import Pipeline, Step

# Define your processing functions
def add(x, y):
    return x + y

def compute(step1, x, z):
    return step1 + x - z

# Create a pipeline and add steps

steps = [
    Step(name="step1", func=add),
    Step(name="step2", func=compute),
]

pipeline = Pipeline(steps)

# Run the pipeline
result = pipeline.run(x=1, y=2, z=3)
print(result)  # Output: {'x': 1, 'y': 2, 'z': 3, 'step1': 3, 'step2': 1}
```

Here are some additional examples to demonstrate the capabilities of the Pipeline pattern:

```python
def multiply(x, y):
    return x * y

def subtract(step1, z):
    return step1 - z

# Create a new pipeline
pipeline = Pipeline()
pipeline.add_step(Step(name="step1", func=multiply))
pipeline.add_step(Step(name="step2", func=subtract))

# Run the pipeline
result = pipeline.run(x=2, y=3, z=1)
print(result)  # Output: {'x': 2, 'y': 3, 'z': 1, 'step1': 6, 'step2': 5}

```