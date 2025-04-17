import sqlite3
import matplotlib.pyplot as plt

# Connect to in-memory SQLite database
conn = sqlite3.connect(':memory:')
cursor = conn.cursor()

# Create table
cursor.execute('''
    CREATE TABLE sales (
        id INTEGER PRIMARY KEY,
        item TEXT,
        quantity INTEGER,
        price REAL
    )
''')

# Sample data
sales_data = [
    ('Pen', 10, 1.5),
    ('Notebook', 5, 3.0),
    ('Pencil', 20, 0.5),
    ('Eraser', 15, 0.75)
]

cursor.executemany('INSERT INTO sales (item, quantity, price) VALUES (?, ?, ?)', sales_data)
conn.commit()

# SQL to get total quantity and revenue per item
cursor.execute('''
    SELECT item, SUM(quantity) as total_quantity, SUM(quantity * price) as total_revenue
    FROM sales
    GROUP BY item
''')

results = cursor.fetchall()

# Print output
print("=== Sales Summary ===")
for item, qty, revenue in results:
    print(f"Item: {item}, Total Quantity Sold: {qty}, Total Revenue: ${revenue:.2f}")

# Prepare data for charts
items = [row[0] for row in results]
quantities = [row[1] for row in results]
revenues = [row[2] for row in results]

# Create side-by-side bar charts
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Quantity Bar Chart
ax1.bar(items, quantities, color='lightgreen')
ax1.set_title("Total Quantity Sold")
ax1.set_xlabel("Item")
ax1.set_ylabel("Quantity")

# Revenue Bar Chart
ax2.bar(items, revenues, color='skyblue')
ax2.set_title("Total Revenue")
ax2.set_xlabel("Item")
ax2.set_ylabel("Revenue ($)")

# Save the chart as a PNG file
plt.tight_layout()
plt.savefig("sales_summary.png")  # 💾 Save chart to file
plt.show()

# Close connection
conn.close()
