import pandas as pd
import oracledb

# Set up data base
LIB_DIR = r"D:\Documents\#School\Oracle_Basic_Light_Package\instantclient_23_0"
DB_USER = "system"
DB_PASS = "7370"
DB_DSN = "127.0.0.1:1521/xe"

oracledb.init_oracle_client(lib_dir=LIB_DIR)

conn = oracledb.connect(user=DB_USER, password=DB_PASS, dsn=DB_DSN)
cursor = conn.cursor()

try:
    # Load CSV files
    crops = pd.read_csv("data/crops.csv")
    locations = pd.read_csv("data/locations.csv")
    conditions = pd.read_csv("data/yearly_conditions.csv")
    yields = pd.read_csv("data/yield_records.csv")

    # Insert crops
    for _, row in crops.iterrows():
        cursor.execute(
            "INSERT INTO crops (crop_id, crop_name) VALUES (:1, :2)",
            (int(row['crop_id']), row['crop_name'])
        )

    # Insert locations
    for _, row in locations.iterrows():
        cursor.execute(
            "INSERT INTO locations (location_id, country) VALUES (:1, :2)",
            (int(row['location_id']), row['country'])
        )

    # Insert yearly_conditions
    for _, row in conditions.iterrows():
        cursor.execute(
            """INSERT INTO yearly_conditions 
            (condition_id, location_id, year, avg_rainfall, avg_temp, tonnes_pesticide)
            VALUES (:1, :2, :3, :4, :5, :6)""",
            (int(row['condition_id']), int(row['location_id']), int(row['year']), float(row['avg_rainfall']), float(row['avg_temp']), float(row['tonnes_pesticide']))
        )

    # Insert yield_records
    for _, row in yields.iterrows():
        cursor.execute(
            """INSERT INTO yield_records 
            (yield_id, crop_id, location_id, year, hg_per_ha_yield)
            VALUES (:1, :2, :3, :4, :5)""",
            (int(row['yield_id']), int(row['crop_id']), int(row['location_id']), int(row['year']), float(row['hg_per_ha_yield']))
        )

    # Commit changes
    conn.commit()

    print("Data loaded successfully :)")

except Exception as e:
    print(f"Error during loading: {e}")
    if 'conn' in locals():
        conn.rollback()

finally:
    if 'cursor' in locals(): cursor.close()
    if 'conn' in locals(): conn.close()