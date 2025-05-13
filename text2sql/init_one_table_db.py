import sqlite3
from sqlite3 import Error

conn = sqlite3.connect('sample.db')
c = conn.cursor()

# Create a sample table
c.execute('''CREATE TABLE IF NOT EXISTS sales (id INTEGER PRIMARY KEY, date TEXT, region TEXT, revenue REAL)''')

# Insert sample data into the table
c.executemany('''INSERT INTO sales (date, region, revenue) VALUES (?, ?, ?)''', [
    ('2021-01-01', 'North', 1000),
    ('2021-01-02', 'South', 2000),
    ('2021-01-03', 'East', 3000),
    ('2021-01-04', 'West', 4000),
    ('2021-01-05', 'North', 5000),
    ('2021-01-06', 'South', 6000),
    ('2021-01-07', 'East', 7000),
    ('2021-01-08', 'West', 8000),
    ('2021-01-09', 'North', 9000),
    ('2021-01-10', 'South', 10000),
    ('2024-03-01', 'North', 1000),
    ('2024-03-02', 'South', 2000),
    ('2024-03-03', 'East', 3000),
    ('2024-03-04', 'West', 4000),
    ('2024-04-04', 'West', 4000),
    ('2024-04-05', 'North', 5000),
    ('2024-07-36', 'South', 6000),
    ('2024-07-37', 'East', 7000),
    ('2024-07-38', 'West', 8000),
    ('2024-07-39', 'North', 9000),
    ('2024-07-40', 'South', 10000),

])

conn.commit()
c.execute("SELECT * FROM sales")
print(c.fetchall())

conn.close()
