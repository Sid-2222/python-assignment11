import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

DB_PATH = "../db/lesson.db"

query = """
    SELECT last_name, SUM(price * quantity) AS revenue
    FROM employees e
    JOIN orders o ON e.employee_id = o.employee_id
    JOIN line_items l ON o.order_id = l.order_id
    JOIN products p ON l.product_id = p.product_id
    GROUP BY e.employee_id;
    """

try:
    with sqlite3.connect(DB_PATH) as conn:
        print("Connected successfully")

        employee_results = pd.read_sql_query(query, conn)

    #print(employee_results)

except sqlite3.Error as e:
    print("Database error:", e)
    exit()

except Exception as e:
    print("Error:", e)
    exit()
    
plt.figure(figsize=(10, 6))
plt.bar(employee_results["last_name"], employee_results["revenue"], color="steelblue",edgecolor="black",linewidth=0.8)
plt.title("Employee Revenue Performance", fontsize=16, fontweight="bold", pad=12)
plt.xlabel("Employee Last Name",fontsize=12,color="tomato")
plt.ylabel("Revenue ($)", fontsize=12)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()