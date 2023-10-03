# Real time E-commerce sales

This project focuses on create a real-time e-commerce. I'll use fake data to simulate the sales. Apache Airflow will be used to schedule the data pipeline.

Help from:

- [Pandas](https://pandas.pydata.org/docs/)
- [PandaSQL](https://pypi.org/project/pandasql/)
- [Poetry](https://python-poetry.org/docs/)
- [Airflow](https://airflow.apache.org/docs/)
- [Faker](https://faker.readthedocs.io/en/master/)
- [Pytest](https://docs.pytest.org/en/7.1.x/contents.html)
- [MySQL](https://dev.mysql.com/doc/connector-python/en/)

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
poetry add pandas pandasql apache-airflow faker pytest ipykernel mysql-connector-python
# `poetry shell` to access the environment in the terminal and `exit` to exit the environment
```

- Airflow (do not forget to run with Poetry: `poetry run...`)

```bash
# At the project root
# Everytime for a new terminal, must execute the line below to put correctly the AIRFLOW_HOME
export AIRFLOW_HOME=$(pwd)/airflow
airflow db migrate
# And here replace the generated airflow.cfg by the personal one
cp -f backend/airflow.cfg airflow/
airflow users create --username admin --firstname admin --lastname admin --role Admin --email admin --password admin

# To see the users
airflow users list

# To run the webserver and the scheduler
airflow webserver -p 8080
airflow scheduler
```

```bash
# Some parameters changed made in the airflow.cfg
# No need to change the default_time, it is utc which is recommended
executor = LocalExecutor
load_examples = False
expose_config = True
```

### 1. Create the Python script(s)

- The generation of fake data is done using Faker, in the gen_fake_data.py file.

### 2. Create DAG (Directed Acyclic Graph)

To generate continuously the data, DAGs need to be created. To perform this task, I decided to schedule the DAG for data generation every minute (so is the data processing). The DAGs are created in the `airflow\dags` folder.
Therefore, the `transaction_dag.py` file must be located in the `airflow\dags` folder.

### Where I got a bit stuck / Interesting points

- The `pandasql` library uses SQLite syntax. Any pandas dataframes will be detected.
- For the data manipulation, I used the `pandasql` library. It allows to use SQL queries on pandas dataframes.
- For the data visualization, I used the `matplotlib` library to plot the data and `mysql-connector-python` to retrieve the data from the database.
- Have to be careful with the `faker` library. Especially with the data generated. Did some researches to understand the use of the seed. But after some tests, I decided to give up on the seed. I admit that the order made is done by the same customer generated.
- When we use SQL queries with `mysql`, the values must be %s (and not %d for example).
- The order of table creation or deletion is important. For instance, if we decide to create a table but it contains foreign keys, we need to create the table(s) with the foreign keys first.
- To access MySQL in the terminal, we need to use the command `mysql -u root -p` and then enter the password.
- To see the schemas of the tables, we can use the command `DESCRIBE table_name;`.
- For the function `mysql.connector.connect`, we need to specify the database name in the `database` parameter. By default, I used `mysql` for the first connection (to create the `e_commerce` database).
- **WARNING for Windows Users**: `pwd` module does not work on Windows as it is a UNIX only package for managing passwords (used to start the airflow server...).

### Extra: Setup of Makefile

```bash
# To run everything
make # or make all

# To run tests
make test
```

### Extra: Setup of pytest

Once the test files are written, we can run the tests.

```bash
pip install pytest

# To run tests
pytest
```

### Extra: Setup of pre-commit

```bash
pip install pre-commit
```

Once the `.pre-commit-config.yaml` completed, we need to set up the git hooks scripts.

```bash
pre-commit install
```
