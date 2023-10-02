from typing import List

import mysql.connector
import pandas as pd
from gen_fake_data import RANDOM_OBJECT_LIST, get_fake_data, get_fake_product


################################################
### --------------- DATABASE --------------- ###
################################################
def connect_database(database_name: str):
    """Connects to the database.

    Args:
        database_name (str): The name of the database.

    Returns:
        The connection.
    """
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database=database_name,
        )
        return mydb
    except mysql.connector.Error:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
        )
        print("Cannot connect to database, connexion without database")
        return mydb


def create_database(database_name: str, cursor) -> None:
    """Creates a database if it doesn't exist.

    Args:
        database_name (str): The name of the database.
        cursor: The cursor of the database.
    """
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")


def show_databases(cursor) -> None:
    """Shows the databases.

    Args:
        cursor: The cursor of the database.
    """
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
            description VARCHAR(255)
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
            customer_id INT,
            product_id INT,
            FOREIGN KEY (customer_id)
                REFERENCES customers(customer_id)
                ON DELETE CASCADE,
            FOREIGN KEY (product_id)
                REFERENCES products(product_id)
                ON DELETE CASCADE
        )
        """
    )


def create_table(table_name: str, cursor) -> None:
    """Creates a table if it doesn't exist.

    Args:
        table_name (str): The name of the table.
        cursor: The cursor of the database.

    Raises:
        ValueError: If the table name is invalid.
    """
    if table_name == "customers":
        _create_table_customers(cursor)
    elif table_name == "orders":
        _create_table_orders(cursor)
    elif table_name == "products":
        _create_table_products(cursor)
    else:
        raise ValueError("Invalid table name")


def show_tables(cursor) -> None:
    """Shows the tables.

    Args:
        cursor: The cursor of the database.
    """
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
    create_table("products", mycursor)
    create_table("customers", mycursor)
    create_table("orders", mycursor)

    # Fill the table's products with fake data
    process_products(mycursor)
    mydb.commit()

    # Once the process is done, close the database
    mycursor.close()
    mydb.close()


def clear_project() -> None:
    """clears the project."""
    # Connect to the database
    mydb = connect_database("e_commerce")
    mycursor = mydb.cursor()

    # Delete the database if it exists
    # mycursor.execute("DROP DATABASE IF EXISTS e_commerce")

    # Delete the tables if they exist
    mycursor.execute("DROP TABLE IF EXISTS orders")
    mycursor.execute("DROP TABLE IF EXISTS customers")
    mycursor.execute("DROP TABLE IF EXISTS products")

    # Once the process is done, close the database
    mycursor.close()
    mydb.close()


def process_products(cursor) -> None:
    """Processes the products.

    Args:
        cursor: The cursor of the database.
    """
    cursor.execute("SELECT COUNT(DISTINCT name) FROM products")
    products = cursor.fetchall()
    while products[0][0] < len(RANDOM_OBJECT_LIST):
        # Generate fake product
        product = get_fake_product()

        # Save the data (we don't to transform the data)
        cursor.execute(
            """
            INSERT INTO products (name, price, description)
            VALUES (%s, %s, %s)
            """,
            (product["name"], product["price"], product["description"]),
        )
        cursor.execute("SELECT COUNT(DISTINCT name) FROM products")
        products = cursor.fetchall()


def process_transaction(data: List[dict]) -> None:
    """Processes the transaction.

    Args:
        data (List[dict]): A list of dictionaries containing fake data.
    """
    mydb = connect_database("e_commerce")
    mycursor = mydb.cursor()

    # Generate fake data (consider there's one transaction per cycle)
    data = get_fake_data()

    # Transformation here is just a replacement of \n by a comma
    data[0]["address"].replace("\n", ", ")

    # Save the data
    save_data(data, mycursor)
    mydb.commit()

    # Once the process is done, close the database
    mycursor.close()
    mydb.close()


def save_data(data: List[dict], cursor):
    """Saves the data.

    Args:
        data (List[dict]): A list of dictionaries containing fake data.
        cursor: The cursor of the database.
    """
    # Save the data
    cursor.execute(
        """
        INSERT INTO customers (name, address, email, phone_number, country)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (
            data[0]["name"],
            data[0]["address"],
            data[0]["email"],
            data[0]["phone_number"],
            data[0]["country"],
        ),
    )
    cursor.execute(
        """
        INSERT INTO orders (order_date, quantity, product)
        VALUES (%s, %d, %s)
        """,
        (data[1]["order_date"], data[1]["quantity"], data[1]["product"]),
    )
