import csv
from analyzer import SalesAnalyzer

class DataExporter:
    def __init__(self, source_csv, output_csv):
        self.source_csv = source_csv
        self.output_csv = output_csv
        
    def export_cleaned_data(self):
        analyzer = SalesAnalyzer(self.source_csv)
        if not analyzer.load_and_clean():
            return 0
        
        fieldnames = ["order_id", "date", "product", "quantity", "total"]
        with open(self.output_csv, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(analyzer.records)
            
        return len(analyzer.records)
    
if __name__=="__main__":
    exporter = DataExporter("sales_data.csv", "cleaned_sales.csv")
    count = exporter.export_cleaned_data()
    print(f"Exported {count} validated records to cleaned_sales.csv")
            