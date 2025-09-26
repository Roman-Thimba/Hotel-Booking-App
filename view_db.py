import sqlite3
import os

# Find the correct database file
db_path = 'instance/hotel_booking.db'
if not os.path.exists(db_path):
    db_path = 'hotel_booking.db'

print(f"Using database: {db_path}")
print(f"Database exists: {os.path.exists(db_path)}")

if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    print(f"\n=== TABLES IN DATABASE ===")
    for table in tables:
        table_name = table[0]
        print(f"\n--- {table_name.upper()} ---")
        
        # Get all data from table
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        
        # Get column names
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = [col[1] for col in cursor.fetchall()]
        
        print(f"Columns: {', '.join(columns)}")
        print(f"Rows: {len(rows)}")
        
        for row in rows:
            print(f"  {dict(zip(columns, row))}")
    
    conn.close()
else:
    print("Database file not found!")