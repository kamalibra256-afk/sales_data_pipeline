import random
import csv
from datetime import datetime,timedelta

products = ["Laptop", "Mouse", "Keyboard", "Monitor", "Headset", "Webcam"]
prices = {"Laptop": 850, "Mouse":25, "Keyboard": 60, "Monitor": 220, "Headset": 80, "Webcam":55}
          
with open("sales_data.csv", mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Order_ID", "Date", "Product", "Quantity", "Unit_Price", "Total_Sales"])
    start_date = datetime(2026, 1, 1)
    for order_id in range(1001, 2001):
        product = random.choice(products)
        qty = random.randint(1, 5)
        price = prices[product]
        total = qty * price
        date_str = (start_date + timedelta(days=random.randint(0,300))).strftime("%Y-%m-%d")
        writer.writerow([order_id, date_str, product, qty, price, total])
    
print("Success! 1,000 rows saved to sales_data.csv")
    