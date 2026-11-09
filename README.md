# Sales Data pipeline

A modular python CLIpipeline for generating,cleaning, and analyzing product sales records.

## Python Automatic engine
- 'main.py' : Automates the  Generation 1,000 initial mock sales record into 'sales_data.csv' . 
- 'analyzer.py' : Validates rows, computes product revenue, and exports 'summary_report.json' .
- 'test_analyzer.py' : Automated unit test suite verifying data cleaning and aggregation.
- 'cli.py' : Interactive command-line control centre to run all pipeline modules and tests.
- 'exporter.py' :Exports Validated sales record into 'cleaned_sales.csv'
- 'trends.py' : Calculates monthly revenue totals and identifies the peak sales day in 'trends_report.json'.
- 'charts.py' : Renders an ASCII revenue bar chart in the terminal from 'summary_report.json'.

## Advanced Excel Entry Interface
- 'advanced_excel_model.py' : Generates a three-sheet interactive templates book('advanced_sales_model.xlst') containing:
   - **Dashboard**:Live metric cards ('SUM', 'COUNTIF'), product summary grids and native excel column charts.
   - **Sales_Entry**: Interactive transaction log backed by drop validation, 'VLOOKUP' catalog lookups, and conditional formatting.
   - **Product_Catalog**: Reference matrix driving the whole sale unit cost, price list, and target margins.
- 'excel_loader.py' : Custom sync module that extracts manual spreadsheet transactions and pipes them instantly back into the core python analytics engine.



## How to Run
1. **Launch the Master Control Center:**
'''powershell
& "C:\Users\ADMIN\.local\bin\python3.14.exe" cli.py
'''

2. **Build the Excel Spreadsheet Blueprint:** Run option '1' to clear any old cache, then execute 'advanced_excel_model.py to compile your live template workbook.
3. **Log Interactive Transactions:** Open 'advanced_sales_model.xlsx' inside google sheets or Microsoft Excel, Populate row variables across column A-E and watch formulas calculate your margins live.
4 **Sync Spreadsheet Metrics Back to python:** Run option'5' (or run 'excel_loader.py' directly) to instantly compile your manual entries into your core script analytics, running verification checks and displaying updated charts side-by-side.
   