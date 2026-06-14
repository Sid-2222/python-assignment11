import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

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
print(df.tail())

plt.figure(figsize=(10, 6))
plt.plot(df["order_id"], df["cumulative"], color="steelblue", linewidth=2)
plt.title("Cumulative Revenue Over Time", fontsize=16, fontweight="bold",color="blue", pad=12)
plt.xlabel("Order ID",fontsize=12, fontweight="bold",color="blue")
plt.ylabel("Cumulative Revenue",fontsize=12, fontweight="bold",color="blue")
plt.grid(True, linestyle="--", alpha=0.5)
plt.tight_layout()

plt.show()