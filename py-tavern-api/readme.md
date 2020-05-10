# Getting Started
**If you use PyCharm:**

- clone repo

- Install dependencies

  ```
  pip freeze > requirements.txt
  ```

-   in PyCharm set pytest as default test runner (preferences-tools-python integrated tools-testing-pytest-apply)
-   make sure your  yaml test is  called `test_x.tavern.yaml`, where `x` should be a description of the contained tests



**If you start your own project  and use PyCharm:**

- create new project [using PyCharm] 

- set up virtualenvironment [using PyCharm] 

-   install pytest via PyCharm]
-   install tavern [via PyCharm]
-   install colorlog [via PyCharm]

-   in PyCharm set pytest as default test runner (preferences-tools-python integrated tools-testing-pytest-apply)
-   make sure your  yaml test is  called `test_x.tavern.yaml`, where `x` should be a description of the contained tests

# Tavern Docs

Feel free to read Tavern Docs [Link](#https://tavern.readthedocs.io/en/latest/basics.html)



# Project structure

```
.
├── LICENSE
├── __pycache__
│   ├── conftest.cpython-38-pytest-5.4.1.pyc
│   └── conftest.cpython-38-pytest-5.4.2.pyc
├── conftest.py
├── logging.yaml
├── pytest.ini
├── readme.md
├── requirements.txt
├── tests
│   ├── __init__.py
│   ├── __pycache__
│   ├── api_urls.yaml
│   ├── common.yaml
│   ├── includes.yaml
│   ├── includesA.yaml
│   ├── includesB.yaml
│   ├── test_basics.tavern.yaml
│   ├── test_http.tavern.yaml
│   ├── utils.py
│   └── yaml_basics.yaml
├── venv
│   ├── bin
│   ├── include
│   ├── lib
│   └── pyvenv.cfg
└── zip_code.yaml
```





# Adding folder to PYTHONPATH

To make sure that Tavern can find **external functions** you need to make sure that it is in the Python path. For example, if **utils.py** is in the ‘tests’ folder:

**Incorrect:**

```
 PYTHONPATH=$PYTHONPATH:/tests pytest tests/test_basics.tavern.yaml -q -k ex04
 ...
 E   tavern.util.exceptions.InvalidExtFunctionError: Error importing module utils
 
```

```
PYTHONPATH=$PYTHONPATH:tests pytest tests/test_basics.tavern.yaml -q -k ex04
 ...
zsh: bad substitution
```



**Correct:**

```
 PYTHONPATH=$PYTHONPATH:./tests pytest tests/test_basics.tavern.yaml -q -k ex04
```



You can modify  ~/.bash_profile  to add absolute path to your PYTHONPATH. For Example:

```
export PYTHONPATH="$PYTHONPATH:/Users/maksim/repos/tau-tools-demo/py-tavern-api/tests"
# save and exit
# then run in shell or in PyCharm terminal:
source ~/.bashprofile

```





# Including external files:

Note : common.yaml  must include **only one document**

```

---

name: Common test information
description: Some information for tests
...
```



# Using saved vars

**Incorrect:**

```
id: {user_id}
```

**Correct:**

```

id: "{user_id}"
```



# Printing entire response using logging

**Add this hook**

```python
#conftest.py

def pytest_tavern_beta_after_every_response(expected, response):
    logging.info(f"================= GOT RESPONSE ================== \n\n{dumps(response.json(), indent=4)}")
    pass
```



**Use --log-cli-level  in command line to enable different logging levels. Example**

```
pytest --log-cli-level=ERROR  snippets/test_basics.tavern.yaml
```



**Can also use pytest.ini  to set logging level:**

```
log_cli = 1
log_level = INFO
log_cli_level = INFO
```

