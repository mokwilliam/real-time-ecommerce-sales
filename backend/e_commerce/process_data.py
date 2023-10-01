from typing import List, Union

import mysql.connector
import pandas as pd
from gen_fake_data import get_fake_customer


################################################
### --------------- DATABASE --------------- ###
################################################
def connect_database(database_name: str):
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database=database_name,
        )
    except mysql.connector.Error:
        print("Cannot connect to database")
    else:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
        )
    return mydb


def create_database(database_name: str, cursor) -> None:
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")


def show_databases(cursor) -> None:
    cursor.execute("SHOW DATABASES")
    for x in cursor:
        print(x)


###############################################
#### --------------- TABLE --------------- ####
###############################################
def _create_table_customers(cursor) -> None:
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255),
            address VARCHAR(255),
            email VARCHAR(255),
            phone_number VARCHAR(255),
            country VARCHAR(255)
        )
        """
    )


def _create_table_products(cursor) -> None:
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS products (
            product_id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255),
            price FLOAT,
            description VARCHAR(255),
        )
        """
    )


def _create_table_orders(cursor) -> None:
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS orders (
            order_id INT AUTO_INCREMENT PRIMARY KEY,
            order_date DATE,
            quantity INT,
            bill FLOAT,
            customer_id INT FOREIGN KEY,
            product_id INT FOREIGN KEY,
        )
        """
    )


def create_table(table_name: str, cursor) -> None:
    if table_name == "customers":
        _create_table_customers(cursor)
    elif table_name == "orders":
        _create_table_orders(cursor)
    elif table_name == "products":
        _create_table_products(cursor)
    else:
        raise ValueError("Invalid table name")


def show_tables(cursor) -> None:
    cursor.execute("SHOW TABLES")
    for x in cursor:
        print(x)


################################################
### ----------------- DATA ----------------- ###
################################################
def init_project() -> None:
    """Initializes the project."""
    # Connect to the database
    mydb = connect_database("e_commerce")
    mycursor = mydb.cursor()

    # Create the database if it doesn't exist
    create_database("e_commerce", mycursor)

    # Create the tables if they don't exist
    create_table("customers", mycursor)
    create_table("orders", mycursor)
    create_table("products", mycursor)

    # TODO: Fill the table's products with fake data

    # Once the process is done, close the database
    mycursor.close()
    mydb.close()


def process_data(data: Union[dict, List[dict]]):  # -> Union[dict, List[dict]]:
    mydb = connect_database("e_commerce")
    mycursor = mydb.cursor()

    # Generate fake data
    # Consider there's one transaction per cycle
    # data = get_fake_data()

    # Transform the data
    # transform_data(data)

    # Save the data
    # save_data(data)

    # Once the process is done, close the database
    mycursor.close()
    mydb.close()


def transform_data(data: List[dict]):
    df_customer = pd.DataFrame(data[0])
    df_product = pd.DataFrame(data[1])
    df_order = pd.DataFrame(data[2])


def save_data(data: Union[dict, List[dict]]):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="e_commerce",
    )
    mycursor = mydb.cursor()

    mydb.close()
