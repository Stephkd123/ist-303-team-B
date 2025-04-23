# import sqlite3
# import pandas as pd
# import os


# # connection = sqlite3.connect('database.db')


# # with open('schema.sql') as f:
# #     connection.executescript(f.read())

# # cur = connection.cursor()

# # cur.execute("INSERT INTO users (username, password) VALUES (?, ?)",
# #             ('userA', 'password123') )
            

# # connection.commit()
# # connection.close()

# # Remove old DB if it exists
# if os.path.exists("la_transit.db"):
#     os.remove("la_transit.db")
#     print("Old database removed.")

# # Reconnect to create a fresh DB
# db = sqlite3.connect("la_transit.db")
# cursor = db.cursor()

# # Load schema from file
# with open("gtfs_schema.sql", "r") as f:
#     schema_sql = f.read()
#     cursor.executescript(schema_sql)
#     print("Schema recreated.")

# # Load GTFS data files
# gtfs_files = [
#     'stops', 'routes', 'trips', 'stop_times', 'calendar', 'agency', 'shapes', 'transfers'
# ]

# for file in gtfs_files:
#     file_path = f"/Users/stephenkeyen/Documents/ist-303-team-B/la_county/{file}.txt"
#     try:
#         df = pd.read_csv(file_path)
#         df.to_sql(file, db, if_exists='append', index=False)
#         print(f"{file} loaded successfully.")
#     except Exception as e:
#         print(f"Error loading {file}: {e}")

# db.commit()
# db.close()

import sqlite3
import pandas as pd
import os

# Delete the DB first to start fresh
if os.path.exists("la_transit.db"):
    os.remove("la_transit.db")
    print("Old database removed.")

# Recreate a fresh DB
db = sqlite3.connect("la_transit.db")

# List of GTFS files
gtfs_files = [
    'stops', 'routes', 'trips', 'stop_times',
    'calendar', 'agency', 'shapes', 'transfers'
]

# Load GTFS files into fresh tables
for file in gtfs_files:
    try:
        df = pd.read_csv(f"/Users/stephenkeyen/Documents/ist-303-team-B/la_county/{file}.txt")
        df.columns = df.columns.str.strip().str.lower()  # normalize column names
        df.to_sql(file.lower(), db, if_exists='replace', index=False)
        print(f"{file} loaded successfully.")
    except Exception as e:
        print(f"Error loading {file}: {e}")

db.commit()
db.close()
