import pandas as pd
import oracledb

# Set up data base
LIB_DIR = r"C:\oracle\instantclient\instantclient_23_0"
DB_USER = "HSYMANSKI10204_SCHEMA_KBVED"
DB_PASS = "QWJOUK4FRN9FDWN3!322ORKM4O6KeB"
DB_DSN = "db.freesql.com:1521/23ai_34ui2"

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
    cursor.executemany(
        "INSERT INTO crops (crop_id, crop_name) VALUES (:1, :2)",
        [(int(r.crop_id), r.crop_name) for r in crops.itertuples(index=False)]
    )
    # Insert locations
    cursor.executemany(
        "INSERT INTO locations (location_id, country) VALUES (:1, :2)",
        [(int(r.location_id), r.country) for r in locations.itertuples(index=False)]
    )
    # Insert yearly_conditions
    cursor.executemany("""
                       INSERT INTO yearly_conditions
                       (condition_id, location_id, year, avg_rainfall, avg_temp, tonnes_pesticide)
                       VALUES (:1, :2, :3, :4, :5, :6)
                       """, [
                           (
                               int(r.condition_id),
                               int(r.location_id),
                               int(r.year),
                               float(r.avg_rainfall),
                               float(r.avg_temp),
                               float(r.tonnes_pesticide) if pd.notna(r.tonnes_pesticide) else None
                           )
                           for r in conditions.itertuples(index=False)
                       ])
    # Insert yield_records
    cursor.executemany("""
                       INSERT INTO yield_records
                           (yield_id, crop_id, location_id, year, hg_per_ha_yield)
                       VALUES (:1, :2, :3, :4, :5)
                       """, [
                           (
                               int(r.yield_id),
                               int(r.crop_id),
                               int(r.location_id),
                               int(r.year),
                               float(r.hg_per_ha_yield)
                           )
                           for r in yields.itertuples(index=False)
                       ])

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