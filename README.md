# Todos API Tests

Simple test suite for the Todos API

---

## Description

This project tests the Todos API.  
It uses **pytest** for execution and **Allure** for reports.

The suite includse:
- Positive tests
- Negative tests
- Payload validation scenarios

---

## Requirements
- Python 3.10 or higher
- pip
- Allure (for reports)

---

## Setup

Install project dependencies:

```bash
pip install -r requirements.txt 
```


## Run tests

Run pytest and save Allure results:
```bash
python -m pytest -vv tests/test_todos.py 
```


## Allure report

Generate static report:

```bash
allure generate allure-results -o allure-report --clean
```

## Open the report:
```bash
allure open allure-report
```

## Remove the report:
```bash
Remove-Item -Recurse -Force allure-results
``` 