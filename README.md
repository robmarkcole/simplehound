# simplehound
Unofficial python API for Sighthound

* For use with https://github.com/robmarkcole/HASS-Sighthound

## Development
* Create venv -> `$ python3 -m venv venv`
* Use venv -> `$ source venv/bin/activate`
* Install requirements -> `$ pip install -r requirements.txt` & `$ pip install -r requirements-dev.txt`
* Run tests -> `$ venv/bin/pytest tests/*`
* Black format with `venv/bin/black simplehound/core.py` and `venv/bin/black tests/test_simplehound.py`