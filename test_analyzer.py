import unittest
import os
import csv
from analyzer import SalesAnalyzer
from trends import SalesTrends
from exporter import DataExporter

class TestSalesAnalyzer(unittest.TestCase):
    def setUp(self):
        self.test_csv = "temp_test_sales.csv"
        with open(self.test_csv, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Order_ID", "Date", "Product", "Quantity", "Unit_Price", "Total_Sales"])
            writer.writerow(["1", "2026-05-01", "Laptop", "2", "850", "1700", ])
            writer.writerow(["2", "2026-05-02", "Mouse", "-1", "25", "-25"])
            
    def tearDown(self):
        if os.path.exists(self.test_csv):
            os.remove(self.test_csv)
            
    def test_cleaning_and_summary(self):
        analyzer = SalesAnalyzer(self.test_csv)
        self.assertTrue(analyzer.load_and_clean())
        summary = analyzer.generate_summary()
        self.assertEqual(summary["total_valid_orders"], 1)
        self.assertEqual(summary["rejected_rows"], 1)
        self.assertEqual(summary["total_revenue"], 1700.0)
        
    def test_monthly_trends(self):
        trends = SalesTrends(self.test_csv)
        results = trends.analyze_trends()
        self.assertEqual(results["monthly_revenue"]["2026-05"], 1675.0)
        self.assertEqual(results["best_sales_day"]["date"], "2026-05-01")
        
    def test_data_exporter(self):
        output_csv = "temp_cleaned.csv"
        exporter = DataExporter(self.test_csv, output_csv)
        count = exporter.export_cleaned_data()
        self.assertEqual(count, 1)
        if os.path.exists(output_csv):
             os.remove(output_csv)
        
if __name__ == "__main__":
    unittest.main()
        