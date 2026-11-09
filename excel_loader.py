import csv
import json
from openpyxl import load_workbook
from analyzer import SalesAnalyzer
from trends import SalesTrends
from charts import RevenueChart
from activity_logger import log_activity

def sync_excel_to_pipeline(xlst_file="advanced_sales_model.xlsx", csv_out="sales_data.csv"):
    #Read the data back from your manual spreadsheet entries
    wb = load_workbook(xlst_file, data_only=True)
    
    #Target your Sales_Entry tab
    if "Sales_Entry" not in wb.sheetnames:
        print("Error: Sales_Entry sheet not found!")
        return
    
    ws = wb["Sales_Entry"]
    rows_written = 0
    
    with open(csv_out, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Order_ID", "Date", "Product", "Quantity", "Unit_Price", "Total_Sales"])
        
        #Read manually entered rows
        for row in ws.iter_rows(min_row=2, values_only=True):
            order_id, date_val, product, cat, qty, price, total = row[:7]
            if order_id is None or product is None or qty is None:
                continue
            
            date_str = str(date_val)[:10]
            
            #formatting carefully
            try:
                qty_value = int(qty)
                price_value = float(price or 0)
                
                if total is not None and str(total).strip() !="" and not str(total).startswith("="):
                    total_val = float(total)
                else:
                    total_val = qty_value * price_value
            except ValueError:
                continue
            writer.writerow([order_id, date_str, product, qty_value, price_value, total_val])
            rows_written +=1
            
    log_activity(f"Excel sync: Extracted {rows_written} manual rows into sales_data.csv")
    
    #triggering python analytics on new entries
    print("[Pipeline] Running automated data cleaning analysis...")
    analyzer = SalesAnalyzer(csv_out)
    if analyzer.load_and_clean():
        report = analyzer.generate_summary()
        with open("summary_report.json", "w") as out:
            json.dump(report, out, indent=4)
            
    print("[Pipeline] Computing updated time-series trends...")
    trends = SalesTrends(csv_out)
    trend_results = trends.analyze_trends()
    with open("trends_report.json", "w") as out:
        json.dump(trend_results, out, indent=4)
        
    #display dashboardterminals
    print("\n[Dashboard] Rendering updated terminal charts:")
    chart = RevenueChart("summary_report.json", "trends_report.json")
    chart.display_product_chart()
    chart.display_monthly_chart()
    
if __name__ == "__main__":
    sync_excel_to_pipeline()
            