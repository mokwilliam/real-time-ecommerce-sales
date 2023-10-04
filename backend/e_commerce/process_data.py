from typing import List

import mysql.connector
import pandas as pd
from e_commerce.gen_fake_data import RANDOM_OBJECT_LIST, get_fake_data, get_fake_product


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
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database=database_name,
    )
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
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="mysql",
    )
    mycursor = mydb.cursor()

    # Create the database if it doesn't exist
    create_database("e_commerce", mycursor)

    # Use the database
    mycursor.execute("USE e_commerce")

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
    while len(RANDOM_OBJECT_LIST) > 0:
        # Generate fake product
        product = get_fake_product()

        if product["name"] in RANDOM_OBJECT_LIST:
            RANDOM_OBJECT_LIST.remove(product["name"])
            # Save the data (we don't to transform the data)
            cursor.execute(
                """
                INSERT INTO products (name, price, description)
                VALUES (%s, %s, %s)
                """,
                (product["name"], product["price"], product["description"]),
            )


def process_transaction() -> None:
    """Processes the transaction."""
    mydb = connect_database("e_commerce")
    mycursor = mydb.cursor()

    # Generate fake data (consider there's one transaction per cycle)
    data = get_fake_data()

    # Transformation here is just a replacement of \n by a comma
    data[0].update({"address": data[0]["address"].replace("\n", ", ")})

    # Save the data
    save_data(data, mydb, mycursor)
    mydb.commit()

    # Once the process is done, close the database
    mycursor.close()
    mydb.close()


def save_data(data: List[dict], db, cursor):
    """Saves the data.

    Args:
        data (List[dict]): A list of dictionaries containing fake data.
        cursor: The cursor of the database.
    """
    # Save the data
    cursor.execute(
        f"""
        SELECT customer_id, name
        FROM customers
        WHERE name = '{data[0]['name']}'
        """
    )
    customer = cursor.fetchall()
    if customer == []:
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
        db.commit()
        cursor.execute(
            f"""
            SELECT customer_id
            FROM customers
            WHERE name = '{data[0]['name']}'
            """
        )
        customer_id = cursor.fetchall()[0][0]
    else:
        customer_id = customer[0][0]
    cursor.execute(
        f"""
        SELECT product_id, price
        FROM products
        WHERE name = '{data[1]['product']}'
        """
    )
    product_id = cursor.fetchall()[0]
    cursor.execute(
        """
        INSERT INTO orders (order_date, quantity, bill, customer_id, product_id)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (
            data[1]["order_date"],
            data[1]["quantity"],
            data[1]["quantity"] * product_id[1],
            customer_id,
            product_id[0],
        ),
    )
