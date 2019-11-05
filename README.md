[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![PyPI Version](https://img.shields.io/pypi/v/simplehound.svg)](https://pypi.org/project/simplehound/)
[![build status](http://img.shields.io/travis/robmarkcole/simplehound/master.svg?style=flat)](https://travis-ci.org/robmarkcole/simplehound)

# simplehound
Unofficial python API for Sighthound, providing helper functions and classes for processing images and parsing the data returned by Sighthound cloud. See the `usage.ipynb` notebook for usage.

## Development
* Create venv -> `$ python3 -m venv venv`
* Use venv -> `$ source venv/bin/activate`
* Install requirements -> `$ pip install -r requirements.txt` & `$ pip install -r requirements-dev.txt`
* Run tests -> `$ venv/bin/py.test --cov=simplehound tests/`
* Black format -> `$ venv/bin/black simplehound/core.py` and `$ venv/bin/black tests/test_simplehound.py` (or setup VScode for format on save)
* Sort imports -> `$ venv/bin/isort simplehound/core.py`