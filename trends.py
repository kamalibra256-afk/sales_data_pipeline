import csv
import json
from collections import defaultdict

class SalesTrends:
    def __init__(self, filepath):
        self.filepath = filepath
        self.monthly_revenue = defaultdict(float)
        self.daily_revenue = defaultdict(float)
        
    def analyze_trends(self):
        with open(self.filepath, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                date_str = row["Date"]
                month_key = date_str[:7]
                total = float(row["Total_Sales"])
                self.monthly_revenue[month_key] += total
                self.daily_revenue[date_str] += total
                
        best_day = max(self.daily_revenue.items(), key=lambda x: x[1])
        sorted_months = dict(sorted(self.monthly_revenue.items()))
        
        return {
            "monthly_revenue": {m: round(v, 2) for m, v in sorted_months.items()},
            "best_sales_day": {"date": best_day[0], "revenue": round(best_day[1], 2)}
        }
        
if __name__ == "__main__":
    trends = SalesTrends("sales_data.csv")
    results = trends.analyze_trends()
    with open("trends_report.json", "w") as out:
        json.dump(results, out, indent=4)
    print("Trends Report:", json.dumps(results, indent=2))