# init_database_SQLite.py
import sqlite3
from sqlite3 import Error

def create_connection():
    """Create a database connection to SQLite database"""
    conn = None
    try:
        conn = sqlite3.connect('rag1.db')
        print(f"Connected to SQLite version {sqlite3.version}")
        return conn
    except Error as e:
        print(e)
    
def create_tables(conn):
    """Create all tables"""
    sql_create_customers = """
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE
    );"""
    
    sql_create_products = """
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price REAL CHECK(price > 0)
    );"""
    
    sql_create_orders = """
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER NOT NULL,
        order_date TEXT,
        FOREIGN KEY (customer_id) REFERENCES customers (id)
    );"""
    
    sql_create_order_items = """
    CREATE TABLE IF NOT EXISTS order_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        quantity INTEGER CHECK(quantity > 0),
        FOREIGN KEY (order_id) REFERENCES orders (id),
        FOREIGN KEY (product_id) REFERENCES products (id)
    );"""
    
    try:
        c = conn.cursor()
        c.execute(sql_create_customers)
        c.execute(sql_create_products)
        c.execute(sql_create_orders)
        c.execute(sql_create_order_items)
        print("Tables created successfully")
    except Error as e:
        print(e)

def insert_sample_data(conn):
    """Insert sample data into all tables"""
    # Customers
    customers = [
        ('John Doe', 'johnDoe@example.com'),
        ('Jane Smith', 'janeSmith@example.com'),
        ('Bob Johnson', 'bobJohnson@example.com'),
        ('Alice Brown', 'aliceBrown@example.com'),
        ('Tom Wilson', 'tomwilson@example.com'),
        ('Emily Davis', 'emilyDavis@example.com'),
        ('Michael Lee', 'michaelLee@example.com'),
        ('Sophia White', 'sophiaWhite@example.com'),
        ('David Green', 'davidGreen@example.com'),
        ('Olivia Black', 'oliviaBlack@example.com'),
        ('Daniel Gray', 'danielGray@example.com'),
        ('Emma Brown', 'emmaBrown@example.com'),
        ('Sophie White', 'sophiewhite@example.com'),
        ('Liam Green', 'liamGreen@example.com'),
        ('Ava Black', 'avaBlack@example.com'),
        ('Noah Gray', 'noahGray@example.com'),
        ('Mia Brown', 'miaBrown@example.com'),
        ('Charlotte White', 'charlotteWhite@example.com'),
        ('Lucas Green', 'lucasGreen@example.com'),
        ('Harper Black', 'harperBlack@example.com'),
        ('Ethan Gray', 'ethanGray@example.com'),
        ('Avery Brown', 'averyBrown@example.com'),
        ('Isabella White', 'isabellaWhite@example.com'),
        ('Mason Green', 'masonGreen@example.com'),
        ('Scarlett Black', 'scarlettBlack@example.com'),
        ('Logan Gray', 'loganGray@example.com'),
        ('Grace Brown', 'graceBrown@example.com'),
        ('Jackson White', 'jacksonWhite@example.com'),
        ('Elijah Green', 'elijahGreen@example.com'),
        ('Lily Black', 'lilyBlack@example.com'),
        ('Lucas Gray', 'lucasGray@example.com'),
        ('Evelyn Brown', 'evelynBrown@example.com'),
        ('Aiden White', 'aidenWhite@example.com'),
        ('Abigail Green', 'abigailGreen@example.com'),
        ('James Black', 'jamesB@example.com'),
        ('Charlotte Gray', 'charlotteGray@example.com'),
        ('Benjamin Brown', 'benjamin@example.com'),
        ('Amelia White', 'amelia@example.com'),
        ('Elijah Green', 'elijah@example.com'),
        ('Harper Black', 'harper@example.com'),
        ('Oliver Gray', 'oliver@example.com'),
        ('Ella Brown', 'ella@example.com'),
        ('William White', 'william@example.com'),
        ('Charlotte Green', 'charlotte@example.com'),
        ('Henry Black', 'henry@example.com'),
        ('Grace Gray', 'grace@example.com'),
        ('Alexander Brown', 'alexander@example.com'),
        ('Victoria White', 'victoria@example.com'),
        ('Jacob Green', 'jacob@example.com'),
        ('Ava Black', 'ava@example.com'),
        ('Michael Gray', 'michael@example.com'),
        ('Sophia Brown', 'sophia@example.com'),
        ('Daniel White', 'daniel@example.com'),
        ('Olivia Green', 'olivia@example.com'),
        ('Matthew Black', 'matthew@example.com'),
        ('Emily Gray', 'emily@example.com'),
        ('David Brown', 'david@example.com'),
        ('Joseph White', 'joseph@example.com'),
        ('Elizabeth Green', 'elizabeth@example.com'),
        ('Christopher Black', 'christopher@example.com'),
        ('Madison Gray', 'madison@example.com'),
        # ... (add all your customer entries)
    ]
    
    # Products (expanded with construction materials)
    products = [
        ('Steel Beam', 45.99),
        ('Concrete Mix 25kg', 12.50),
        ('Wood Plank (2x4)', 8.75),
        ('Roofing Tiles', 4.99),
        ('Electrical Wiring Kit', 89.99),
        ('Plumbing Fixture Set', 39.99),
        ('Paint (1L)', 14.99),
        ('Screws (Box of 500)', 5.99),
        ('Nails (Box of 500)', 4.99),
        ('Insulation Roll', 19.99),
        ('Cement Bag 50kg', 15.99),
        ('Bricks (Box of 100)', 10.99),
        ('Drywall Sheet', 18.99),
        ('Flooring Tiles', 12.99),
        ('Window Frame', 59.99),
        ('Door Frame', 69.99),
        ('Rebar (10m)', 19.99),
        ('Plywood Sheet', 24.99),
        ('Insulated Pipe', 14.99),

        # ... (add other products)
    ]
    
    # Orders
    orders = [
        (1, '2023-01-15'),
        (2, '2023-02-20'),
        (3, '2023-03-10'),
        (4, '2023-04-05'),
        (5, '2023-05-15'),
        (6, '2023-06-25'),
        (7, '2023-07-10'),
        (8, '2024-08-05'),
        (9, '2024-09-15'),
        (10, '2024-10-25'),
        (11, '2024-11-10'),
        (12, '2024-12-05'),
        (13, '2025-01-15'),
        (14, '2025-02-20'),
        (15, '2025-03-10'),
        (16, '2025-04-05'),
        (17, '2024-09-15'),
        (18, '2024-10-25'),
        (19, '2024-11-10'),
        (20, '2024-12-05'),
        (21, '2025-01-15'),
        (22, '2020-02-20'),
        (23, '2020-03-10'),
        (24, '2020-04-05'),
        (25, '2020-05-15'),
        (26, '2020-06-25'),
        (27, '2020-07-10'),
        (28, '2020-08-05'),
        (29, '2020-09-15'),
        (30, '2020-10-25'),
        (31, '2020-11-10'),
        (32, '2020-12-05'),
        (33, '2020-01-15'),
        (34, '2020-02-20'),
        (35, '2020-03-10'),
        (36, '2020-04-05'),
        (37, '2020-05-15'),
        (38, '2020-06-25'),
        (39, '2020-07-10'),
        (40, '2020-08-05'),
        (41, '2020-09-15'),
        (42, '2020-10-25'),
        (43, '2020-11-10'),
        (44, '2020-12-05'),
        (45, '2020-01-15'),
        (46, '2020-02-20'),
        (47, '2020-03-10'),
        (48, '2020-04-05'),
        (49, '2020-05-15'),
        (50, '2020-06-25'),
        # ... (add order entries)
    ]
    
    # Order Items
    order_items = [
        (1, 1, 10),  # Order 1: 10 Steel Beams
        (1, 3, 50),  # Order 1: 50 Wood Planks
        (2, 2, 20),  # Order 2: 20 Concrete Mixes
        (2, 4, 100), # Order 2: 100 Roofing Tiles
        (3, 5, 2),   # Order 3: 2 Electrical Wiring Kits
        (3, 6, 1),   # Order 3: 1 Plumbing Fixture Set
        (4, 7, 10),  # Order 4: 10 Paints
        (4, 8, 100), # Order 4: 100 Screws
        (5, 9, 50),  # Order 5: 50 Nails
        (5, 10, 10), # Order 5: 10 Insulation Rolls
        (6, 11, 10), # Order 6: 10 Cement Bags
        (6, 12, 100),# Order 6: 100 Bricks
        (7, 13, 10),  # Order 7: 10 Drywall Sheets
        (7, 14, 100), # Order 7: 100 Flooring Tiles
        (8, 15, 10),  # Order 8: 10 Window Frames
        (8, 16, 10),  # Order 8: 10 Door Frames
        (9, 17, 10),  # Order 9: 10 Window Frames
        (9, 18, 10),  # Order 9: 10 Door Frames
        (10, 19, 10), # Order 10: 10 Window Frames
        (10, 20, 10), # Order 10: 10 Door Frames
        (11, 21, 10), # Order 11: 10 Window Frames
        (11, 22, 10), # Order 11: 10 Door Frames
        (12, 23, 10), # Order 12: 10 Window Frames
        (12, 24, 10), # Order 12: 10 Door Frames
        (13, 25, 10), # Order 13: 10 Window Frames
        (13, 26, 10), # Order 13: 10 Door Frames
        (14, 27, 10), # Order 14: 10 Window Frames
        (14, 28, 10), # Order 14: 10 Door Frames
        (15, 29, 10), # Order 15: 10 Window Frames
        (15, 30, 10), # Order 15: 10 Door Frames
        (16, 31, 10), # Order 16: 10 Window Frames
        (16, 32, 10), # Order 16: 10 Door Frames
        (17, 33, 10), # Order 17: 10 Window Frames
        (17, 34, 10), # Order 17: 10 Door Frames
        # ... (add order item entries)
    ]
    
    try:
        c = conn.cursor()
        
        # Insert customers
        c.executemany("INSERT INTO customers (name, email) VALUES (?, ?)", customers)
        
        # Insert products 
        c.executemany("INSERT INTO products (name, price) VALUES (?, ?)", products)
        
        # Insert orders
        c.executemany("INSERT INTO orders (customer_id, order_date) VALUES (?, ?)", orders)
        
        # Insert order items
        c.executemany("INSERT INTO order_items (order_id, product_id, quantity) VALUES (?, ?, ?)", order_items)
        
        conn.commit()
        print("Sample data inserted successfully")
        
    except Error as e:
        print(e)

if __name__ == '__main__':
    conn = create_connection()
    
    if conn is not None:
        create_tables(conn)
        insert_sample_data(conn)
        conn.close()
        print("Database setup complete")
    else:
        print("Error! Cannot create database connection")