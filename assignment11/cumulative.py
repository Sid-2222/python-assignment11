import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.data as pldata
import webbrowser
import os

#Task 2: A Line Plot with Pandas
DB_PATH = "../db/lesson.db"

query = """
        SELECT o.order_id,
        SUM(p.price * l.quantity) AS total_price
        FROM orders o
        JOIN line_items l ON o.order_id = l.order_id
        JOIN products p ON l.product_id = p.product_id
        GROUP BY o.order_id
        ORDER BY o.order_id;
        """

try:
    with sqlite3.connect(DB_PATH) as conn:
        print("Database Connected successfully")
        
        df = pd.read_sql_query(query, conn)

        

except sqlite3.Error as e:
    print("Database error:", e)
    exit()

except Exception as e:
    print("Error:", e)
    exit()
    
df["cumulative"] = df["total_price"].cumsum()

plt.figure(figsize=(10, 6))
plt.plot(df["order_id"], df["cumulative"], color="steelblue", linewidth=2)
plt.title("Cumulative Revenue Over Time", fontsize=16, fontweight="bold",color="blue", pad=12)
plt.xlabel("Order ID",fontsize=12, fontweight="bold",color="blue")
plt.ylabel("Cumulative Revenue",fontsize=12, fontweight="bold",color="blue")
plt.grid(True, linestyle="--", alpha=0.5)
plt.tight_layout()

plt.show()

# Task 3: Interactive Visualizations with Plotly
df = pldata.wind(return_type='pandas')
print("First 10 lines of the DataFrame.")
print(df.head(10))
print("Last 10 lines of the DataFrame.")
print(df.tail(10))

# cleaning data

df["strength"] = df["strength"].str.replace(r"[^\d.]", "", regex=True)
df["strength"] = pd.to_numeric(df["strength"], errors="coerce")
df["frequency"] = pd.to_numeric(df["frequency"], errors="coerce")
df = df.dropna(subset=["strength", "frequency", "direction"])

fig = px.scatter(
    df,
    x="strength",
    y="frequency",
    color="direction",
    title="Wind Strength vs Frequency",
    labels={
        "strength": "Wind Strength",
        "frequency": "Frequency"
    }
)

fig.write_html("wind.html", auto_open=False)
webbrowser.open("file://" + os.path.abspath("wind.html"))


