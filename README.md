# Real time E-commerce sales

This project focuses on create a real-time e-commerce. I'll use fake data to simulate the sales. Apache Airflow will be used to schedule the data pipeline.

Help from:

- [Pandas](https://pandas.pydata.org/docs/)
- [PandaSQL](https://pypi.org/project/pandasql/)
- [Poetry](https://python-poetry.org/docs/)
- [Airflow](https://airflow.apache.org/docs/)
- [Faker](https://faker.readthedocs.io/en/master/)
- [Pytest](https://docs.pytest.org/en/7.1.x/contents.html)

## Overview

In this project, we have a real-time e-commerce sales. Using Python and SQL, the objective is to create a data pipeline to process the data and make it available for the data scientists. Apache Airflow will orchestrate the data generation and processing pipeline, ensuring that data is processed in real-time or at defined intervals.

## Steps followed

### 0. Installation & Setup

- Poetry project

```bash
pip install poetry

# `poetry init --no-interaction` to initialize a pre-existing project
poetry new backend --name="e-commerce"
cd backend
poetry add pandas pandasql apache-airflow faker pytest ipykernel
# `poetry shell` to access the environment in the terminal and `exit` to exit the environment
```

### 1. Create the Python script(s)

- The generation of fake data is done using Faker, in the gen_fake_data.py file.

### 2. Create DAG (Directed Acyclic Graph)

For the dataset, I retrieved data from the following website https://open-meteo.com/ (for more details, go check the [docs](https://open-meteo.com/en/docs)).

```python
# Default arguments for the DAG
# ...

# Create a DAG instance
# ...
```

### Where I got a bit stuck / Interesting points

- The `pandasql` library uses SQLite syntax. Any pandas dataframes will be detected.

### Extra: Setup of Makefile

```bash
# To run everything
make # or make all

# To run tests
make test
```

### Extra: Setup of pytest

```bash
pip install pytest
```

### Extra: Setup of pre-commit

```bash
pip install pre-commit
```

Once the `.pre-commit-config.yaml` completed, we need to set up the git hooks scripts.

```bash
pre-commit install
```
