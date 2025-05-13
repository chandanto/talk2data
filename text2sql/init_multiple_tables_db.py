import sqlite3
from sqlite3 import Error

conn = sqlite3.connect('shop.db')
c = conn.cursor()

# create a customers
c.execute("""CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT
)""")

# Create a products table
c.execute("""CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    price REAL
)""")

# Create a orders table
c.execute("""CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER,
    order_date TEXT,
    FOREIGN KEY(customer_id) REFERENCES customers(id)
)""")


# Create order_items table (junction table)
c.execute("""CREATE TABLE IF NOT EXISTS order_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    FOREIGN KEY(order_id) REFERENCES orders(id),
    FOREIGN KEY(product_id) REFERENCES products(id)
)""")

# Insert data into customers table
c.executemany("INSERT INTO customers (name, email) VALUES (?, ?)", [
    ('John Doe', 'john@example.com'),
    ('Jane Doe', 'jane@example.com'),
    ('Bob Smith', 'bob@example.com'),
    ('Alice Johnson', 'alice@example.com'),
    ('Tom Brown', 'tom@example.com'),
    ('Sara Davis', 'sara@example.com'),
    ('Mike Wilson', 'mike@example.com'),
    ('Emily Taylor', 'emily@example.com'),
    ('David Lee', 'david@example.com'),
    ('Karen White', 'karen@example.com'),
    ('Chris Green', 'chris@example.com'),
    ('Lisa Black', 'lisa@example.com'),
    ('Susan Gray', 'susan@example.com'),
    ('Mark Brown', 'mark@example.com'),
    ('Claire White', 'claire@example.com')
])

# Insert data into products table - products(name) by using electronic devices
c.executemany("INSERT INTO products (name, price) VALUES (?, ?)", [
    ('Laptop', 1000),
    ('Smartphone', 500),
    ('Tablet', 300),
    ('Headphones', 100),
    ('Keyboard', 50),
    ('Mouse', 20),
    ('Monitor', 200),
    ('Printer', 150),
    ('Scanner', 100),
    ('Router', 50),
    ('Speakers', 100),
    ('Camera', 200),
    ('Gamepad', 50),
    ('Microphone', 50),
    ('Webcam', 50),
    ('USB Drive', 20),
    ('SD Card', 10),
    ('HDMI Cable', 10),
    ('Ethernet Cable', 10),
    ('Power Bank', 50),
    ('Charger', 20),
    ('Bluetooth Speaker', 50),
    ('USB Hub', 20),
    ('Wireless Mouse', 20),
    ('Wireless Keyboard', 50),
    ('Wireless Headphones', 100),
    ('Wireless Charger', 50),
    ('Wireless Router', 50),
    ('Wireless Printer', 150),
    ('Wireless Scanner', 100),
    ('Wireless Monitor', 200),
    ('Wireless Gamepad', 50),
    ('Wireless Microphone', 50),
    ('Wireless Webcam', 50),
    ('Wireless USB Drive', 20),
    ('Wireless SD Card', 10),
    ('Wireless HDMI Cable', 10),
    ('Wireless Ethernet Cable', 10),
    ('Wireless Power Bank', 50),
    ('Wireless Charger', 20),
    ('Wireless Bluetooth Speaker', 50),
    ('Wireless USB Hub', 20)
])


# Insert data into orders table
c.executemany("INSERT INTO orders (customer_id, order_date) VALUES (?, ?)", [
    (1, '2020-01-01'),
    (2, '2020-01-02'),
    (3, '2020-01-03'),
    (4, '2021-07-04'),
    (5, '2020-01-05'),
    (6, '2020-01-06'),
    (7, '2022-11-07'),
    (8, '2020-01-08'),
    (9, '2020-01-09'),
    (10, '2022-11-10'),
    (11, '2022-01-11'),
    (12, '2020-01-12'),
    (13, '2022-01-13'),
    (14, '2023-01-14'),
    (15, '2023-01-15'),
    (16, '2024-05-16'),
    (17, '2024-05-17'),
    (18, '2024-05-18'),
    (19, '2024-05-19'),
    (20, '2024-05-20'),
    (21, '2024-05-21'),
    (22, '2024-05-22'),
    (23, '2024-05-23'),
    (24, '2024-05-24'),
    (25, '2024-05-25'),
    (26, '2024-05-26'),
    (27, '2024-05-27'),
    (28, '2024-05-28'),
    (29, '2024-05-29'),
    (30, '2024-05-30'),
    (31, '2025-01-17'),
    (32, '2025-01-18'),
    (33, '2025-01-19'),
    (34, '2025-01-20'),
    (35, '2025-01-21'),
    (36, '2025-01-22'),
    (37, '2025-01-23'),
    (38, '2025-01-24'),
    (39, '2025-01-25'),
    (40, '2025-01-26'),
    (41, '2025-01-27'),
    (42, '2025-01-28'),
    (43, '2025-01-29'),
    (44, '2025-01-30'),
    (45, '2025-02-10'),
    (46, '2025-02-11'),
    (47, '2025-02-12'),
    (48, '2025-02-13'),
    (49, '2025-02-14'),
    (50, '2025-02-15'),
    (51, '2025-02-16'),
    (52, '2025-02-17'),
    (53, '2025-02-18'),
    (54, '2025-02-19'),
    (55, '2025-02-20'),
    (56, '2025-02-21'),
    (57, '2025-02-22'),
    (58, '2025-02-23'),
    (59, '2025-02-24'),
    (60, '2025-02-25'),
    (61, '2025-02-26'),
    (62, '2025-02-27'),
    (63, '2025-02-28'),
    (64, '2025-03-01'),
    (65, '2025-03-02'),
    (66, '2025-03-03'),
    (67, '2025-03-04'),
    (68, '2025-03-05')

])

# Insert data into order_items table
c.executemany("INSERT INTO order_items (order_id, product_id, quantity) VALUES (?, ?, ?)", [
    (1, 1, 1),
    (1, 2, 1),
    (1, 3, 1),
    (2, 4, 1),
    (2, 5, 1),
    (2, 6, 1),
    (3, 7, 1),
    (3, 8, 1),
    (3, 9, 1),
    (4, 10, 1),
    (4, 11, 1),
    (4, 12, 1),
    (5, 13, 1),
    (5, 14, 1),
    (5, 15, 1),
    (6, 16, 1),
    (6, 17, 1),
    (6, 18, 1),
    (7, 19, 1),
    (7, 20, 1),
    (7, 21, 1),
    (8, 22, 1),
    (8, 23, 1),
    (8, 24, 1),
    (9, 25, 1),
    (9, 26, 1),
    (9, 27, 1),
    (10, 28, 1),
    (10, 29, 1),
    (10, 30, 1),
    (11, 31, 1),
    (11, 32, 1),
    (11, 33, 1),
    (12, 34, 1),
    (12, 35, 1),
    (12, 36, 1),
    (13, 37, 1),
    (13, 38, 1),
    (13, 39, 1),
    (14, 40, 1),
    (14, 41, 1),
    (14, 42, 1),
    (15, 43, 1),
    (15, 44, 1),
    (15, 45, 1),
    (16, 46, 1),
    (16, 47, 1),
    (16, 48, 1),
    (17, 49, 1),
    (17, 50, 1),
    (17, 51, 1),
    (18, 52, 1),
    (18, 53, 1),
    (18, 54, 1),
    (19, 55, 1),
    (19, 56, 1),
    (19, 57, 1),
    (20, 58, 1),
    (20, 59, 1),
    (20, 60, 1),
    (21, 61, 1),
    (21, 62, 1),
    (21, 63, 1),
    (22, 64, 1),
    (22, 65, 1),
    (22, 66, 1),
    (23, 67, 1),
    (23, 68, 1),
    (23, 69, 1),
    (24, 70, 1),
    (24, 71, 1),
    (24, 72, 1),
    (25, 73, 1),
    (25, 74, 1),
    (25, 75, 1),
    (26, 76, 1),
    (26, 77, 1),
    (26, 78, 1),
    (27, 79, 1),
    (27, 80, 1),
    (27, 81, 1)

])


conn.commit()
c.execute("SELECT * FROM customers")
print(c.fetchall())
c.execute("SELECT * FROM products")
print(c.fetchall())
c.execute("SELECT * FROM orders")
print(c.fetchall())
c.execute("SELECT * FROM order_items")
print(c.fetchall())

conn.close()
