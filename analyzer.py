import csv
import json
from collections import defaultdict

class SalesAnalyzer:
    def __init__(self,filepath):
        self.filepath = filepath
        self.records = []
        self.errors = []
        
        
    def load_and_clean(self):
        try:
            with open(self.filepath, mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row_num, row in enumerate(reader, start=2):
                    try:
                        qty = int(row["Quantity"])
                        total = float(row["Total_Sales"])
                        if qty <= 0 or total < 0:
                            raise ValueError("Negative or zero value detected")
                        self.records.append({
                            "order_id": row["Order_ID"],
                            "date": row["Date"],
                            "product": row["Product"].strip(),
                            "quantity": qty,
                            "total": total
                        })
                    except (ValueError, KeyError) as e:
                        self.errors.append(f"Row {row_num}: {e}")
        except FileNotFoundError:
            print(f"Critical Error: {self.filepath} not found.")
            return False
        return True

    def generate_summary(self):
        revenue_by_product = defaultdict(float)
        units_by_product = defaultdict(int)
        
        for rec in self.records:
            revenue_by_product[rec["product"]] += rec["total"]
            units_by_product[rec["product"]] += rec["quantity"]
            
        summary = {
            "total_valid_orders": len(self.records),
            "rejected_rows": len(self.errors),
            "total_revenue": round(sum(revenue_by_product.values()), 2),
            "product_breakdown" : {
                prod: {
                    "units_sold": units_by_product[prod],
                    "revenue": round(revenue_by_product[prod], 2)
                }
                for prod in sorted(revenue_by_product.keys())
            }
        }
        return summary

if __name__ == "__main__":
    analyzer = SalesAnalyzer("sales_data.csv")
    if analyzer.load_and_clean():
        report = analyzer.generate_summary()
        with open("summary_report.json", "w") as out:
            json.dump(report, out, indent=4)
        print("Report generated successfully:", json.dumps(report, indent=2))                   
