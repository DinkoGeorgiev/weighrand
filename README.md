# weighrand
A weighted random generator utilizing the python random module.

## Requirements

- Python 3.9+

## Usage

```
from weighrand.randomgen import RandomGen


# Create the random generator
random_gen = RandomGen(random_nums=[1, 2, 3, 4], probabilities=[0.1, 0.2, 0.3, 0.35])

# Generate a random number
generated_number = random_gen.next_num()

# Alternatively, the random generator can be used as iterator.
for random_num in iter(random_gen):
    # Do something
    break
```

## Tests

The recommended way to run the tests is using tox (https://tox.wiki), preferably in a virtual environment.


### Linux
```
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip install tox
$ tox
```
### Windows
```
> py -m venv .venv
> .venv\Scripts\activate.bat
> pip install tox
> set PYTHON_EXE=python && tox
```
_Note: The creation and activation of the virtual environment may vary depending on your setup._

For alternative ways of running the tests, e.g. directly with `pytest`, you may have to install the test requirements first:
```pip install -e .[test]```

## Install

The package can be installed with `pip` from the project root directory.
```
pip install .
```

## TODO

* Implement alternative version using generator function.
* The current implementation prioritizes space over speed. It works well in scenarios that require large number of different probability / choices settings and relatively low number of generation calls. An alternative implementation that trades space for speed would be more suitable when large number of random generations with the same settings are required.
