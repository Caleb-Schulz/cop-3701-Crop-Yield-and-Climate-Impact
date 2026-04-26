# To run 
# pip install streamlit pandas oracledb
# streamlit run magdalene_symanski_parte/app.py

# Data output updated by Caleb to make more appealing

import streamlit as st
import oracledb
import pandas as pd

LIB_DIR = r"C:\oracle\instantclient\instantclient_23_0"

# Your Oracle Credentials
DB_USER = "HSYMANSKI10204_SCHEMA_KBVED"  # or your FreeSQL username
DB_PASS = "QWJOUK4FRN9FDWN3!322ORKM4O6KeB"  # your password for the dbms user
DB_DSN = "db.freesql.com:1521/23ai_34ui2"  # or your FreeSQL DSN

@st.cache_resource
def init_db():
    try:
        oracledb.init_oracle_client(lib_dir=LIB_DIR)
    except Exception:
        pass

def get_connection():
    init_db()
    return oracledb.connect(user=DB_USER, password=DB_PASS, dsn=DB_DSN)

st.set_page_config(layout="wide")

st.title("Crop Yield/Climate Impact Dataset")
# st.subheader("crud duds")

menu = ["Crops Grown by Country",
      "Top Crop by Country",
      "Crop Best Years",
      "Compare Rainfall vs. Yield",
      "Compare Pesticide vs. Yield"]

choice = st.sidebar.selectbox("Select Action", menu)

# ~~~~~~ CROPS GROWN IN EACH COUNTRY (JOIN query 1)

if choice == "Crops Grown by Country":
    st.write("### Crops Grown by Country")

    country = st.text_input("Enter Country")

    if st.button("Search"):
        try:
            conn = get_connection()
            cur = conn.cursor()

            cur.execute("""
                SELECT DISTINCT c.crop_name
                FROM yield_records y
                JOIN crops c ON y.crop_id = c.crop_id
                JOIN locations l ON y.location_id = l.location_id
                WHERE l.country = :1
            """, [country])

            rows = cur.fetchall()
            df = pd.DataFrame(rows, columns=["Crop Name"])
            st.dataframe(df)

            cur.close()
            conn.close()
        except Exception as e:
            st.error(f"Error: {e}")

# ~~~~~~ TOP YIELDING CROPS BY COUNTRY (JOIN query 2)

elif choice == "Top Crop by Country":
    st.write("### Top Crop by Country (hg/ha)")

    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT l.country, c.crop_name, y.hg_per_ha_yield
            FROM yield_records y
            JOIN crops c ON y.crop_id = c.crop_id
            JOIN locations l ON y.location_id = l.location_id
            WHERE (l.country, y.hg_per_ha_yield) IN (
                SELECT l.country, MAX(y.hg_per_ha_yield)
                FROM yield_records y
                JOIN locations l ON y.location_id = l.location_id
                GROUP BY l.country
            )
        """)

        rows = cur.fetchall()
        df = pd.DataFrame(rows, columns=["Country", "Crop Name", "Yield (hg/ha)"])
        st.dataframe(df, use_container_width=True)

        cur.close()
        conn.close()
    except Exception as e:
        st.error(f"Error: {e}")

# ~~~~~~ BEST YEAR FOR EACH CROP (JOIN query 3)

elif choice == "Crop Best Years":
    st.write("### Best Years for Each Crop (hg/ha)")

    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT c.crop_name, y.year, y.hg_per_ha_yield
            FROM yield_records y
            JOIN crops c ON y.crop_id = c.crop_id
            WHERE (y.crop_id, y.hg_per_ha_yield) IN (
                SELECT y.crop_id, MAX(y.hg_per_ha_yield)
                FROM yield_records y
                GROUP BY y.crop_id
            )
        """)

        rows = cur.fetchall()
        df = pd.DataFrame(rows, columns=["Crop Name", "Year", "Yield (hg/ha)"])
        st.dataframe(df, use_container_width=True)

        cur.close()
        conn.close()
    except Exception as e:
        st.error(f"Error: {e}")

# ~~~~~~ RAINFALL (in) vs. CROP YIELD (hgha) (join query 4)

elif choice == "Compare Rainfall vs. Yield":
    st.write("### Rainfall (in) vs. Yield (hg/ha)")

    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT y.year, y.hg_per_ha_yield, yc.avg_rainfall
            FROM yield_records y
            JOIN yearly_conditions yc ON y.location_id = yc.location_id AND y.year = yc.year
            ORDER BY y.year
        """)

        rows = cur.fetchall()
        df = pd.DataFrame(rows, columns=["Year", "Yield (hg/ha)", "Avg Rainfall"])
        # too laggy made static image
        # st.scatter_chart(data=df, x="Avg Rainfall", y="Yield (hg/ha)", color="Year", height=600)
        st.image("magdalene_symanski_parte/graphs/Rainfall_vs._Yield.png", caption="Rainfall vs. Yield Analysis", use_container_width=True)
        st.dataframe(df, use_container_width=True)

        cur.close()
        conn.close()
    except Exception as e:
        st.error(f"Error: {e}")

# ~~~~~~ PESTICIDE USE (gal) vs. CROP YIELD (hgha) (JOIN query 5)

elif choice == "Compare Pesticide vs. Yield":
    st.write("### Pesticide (gal) vs. Yield (hg/ha)")

    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT y.year, y.hg_per_ha_yield, yc.tonnes_pesticide
            FROM yield_records y 
            JOIN yearly_conditions yc ON y.location_id = yc.location_id AND y.year = yc.year
            ORDER BY y.year
        """)

        rows = cur.fetchall()
        df = pd.DataFrame(rows, columns=["Year", "Yield (hg/ha)", "Pesticide (tonnes)"])
        # too laggy made static image
        # st.scatter_chart(data=df, x="Pesticide (tonnes)", y="Yield (hg/ha)",color="Year", height=600)
        st.image("magdalene_symanski_parte/graphs/Pesticide_vs._Yield.png", caption="Pesticide vs. Yield Analysis", use_container_width=True)
        st.dataframe(df, use_container_width=True)

        cur.close()
        conn.close()
    except Exception as e:
        st.error(f"Error: {e}")
