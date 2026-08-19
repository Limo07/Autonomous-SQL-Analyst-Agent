import sqlite3
import pandas as pd

# 1. Create mock vehicle data
data = {
    "vehicle_id": [101, 102, 103, 104, 105],
    "make": ["Toyota", "Honda", "Nissan", "Toyota", "Subaru"],
    "model": ["Supra", "Civic Type R", "Skyline GT-R", "Land Cruiser", "Impreza WRX"],
    "import_year": [2024, 2024, 2025, 2025, 2026],
    "purchase_price_usd": [45000, 38000, 75000, 60000, 25000],
    "sale_price_usd": [52000, 43000, 85000, 71000, 31000],
    "status": ["Sold", "Sold", "In Transit", "Sold", "Available"]
}

df = pd.DataFrame(data)

# 2. Connect to a local SQLite Database
conn = sqlite3.connect("cars.db")

# 3. Write the data to a SQL table named 'inventory'
df.to_sql("inventory", conn, if_exists="replace", index=False)

print("✅ Successfully created cars.db and loaded the 'inventory' table.")
conn.close()