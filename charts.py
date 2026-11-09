import json

class RevenueChart:
    def __init__(self, report_json, trends_json):
        self.report_json = report_json
        self.trends_json = trends_json
        
    def display_product_chart(self):
        with open(self.report_json, mode="r", encoding="utf-8") as file:
            data = json.load(file)
            
        breakdown = data.get("product_breakdown", {})
        if not breakdown:
            print("No data available,")
            return
        
        max_rev = max(item["revenue"] for item in breakdown.values())
        print("\n=== Product Revenue Chart ===")
        for product, stats in breakdown.items():
            rev = stats["revenue"]
            bar_length = int((rev / max_rev) * 30) if max_rev > 0 else 0
            bar = "#" * bar_length
            print(f"{product:<10} | {bar:<30} | ${rev:,.2f}")
            
    def display_monthly_chart(self):
        with open(self.trends_json, mode="r", encoding="utf-8") as file:
            data = json.load(file)
            
        monthly = data.get("monthly_revenue", {})
        if not monthly:
            print("No monthly data available.")
            return
        
        max_rev = max(monthly.values())
        print("\n=== Monthly Revenue Chart ===")
        for month, rev in monthly.items():
            bar_length = int((rev / max_rev) * 30) if max_rev > 0 else 0
            bar = "#" * bar_length
            print(f"{month:<10} | {bar:<30} | ${rev:,.2f}")
            
if __name__ == "__main__":
    chart = RevenueChart("summary_report.json", "trends_report.json")
    chart.display_product_chart()
    chart.display_monthly_chart()