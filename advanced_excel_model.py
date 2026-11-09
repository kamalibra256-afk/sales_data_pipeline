from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import CellIsRule
from openpyxl.chart import BarChart, Reference

def build_advanced_workbook(filename="advanced_sales_model.xlsx"):
    wb = Workbook()
    
    #styling definitions
    header_fill = PatternFill(start_color="1F4E78", end_color="1F4E78", fill_type="solid")
    accent_fill = PatternFill(start_color="D9E1F2", end_color="D9E1F2", fill_type="solid")
    white_bold = Font(bold=True, color="FFFFFF", size=11)
    title_font = Font(bold=True, color="1F4E78", size=14)
    bold_font = Font(bold=True, size=11)
    thin_border = Border(
        left=Side(style="thin", color="D9D9D9"),
        right=Side(style="thin", color="D9D9D9"),
        top=Side(style="thin", color="D9D9D9"),
        bottom=Side(style="thin", color="D9D9D9"),
    )
    
    # Tab 1; Product catalog (Lookup Reference Table)
    ws_cat = wb.active
    ws_cat.title = "Product_Catalog"
    ws_cat.append(["Product", "Category", "Unit_Price"])
    for cell in ws_cat[1]:
        cell.font = white_bold
        cell.fill = header_fill
        
    catalog_items = [
        ["Laptop", "Computers", 850.00],
        ["Monitor", "Displays", 220.00],
        ["Keyboard", "Accessories", 45.00],
        ["Mouse", "Accessories", 25.00],
        ["Webcam", "Peripherals", 55.00],
        ["Headset", "Audio", 70.00],
    ]
    for items in catalog_items:
        ws_cat.append(items)
        
    for rows in ws_cat.iter_rows(min_row=2, max_row=7, min_col=3, max_col=3):
        for cell in rows:
            cell.number_format = "$#,##0.00"
            
    #Tab 2:Sales_Entry (interactive manuaal Entry with Dropdowns and VLOOKUP)
    ws_entry = wb.create_sheet(title="Sales_Entry")
    headers = ["Order_ID", "Date", "Product", "Category", "Quantity", "Unit_Price", "Total_Sales"]
    ws_entry.append(headers)
    for cell in ws_entry[1]:
        cell.font = white_bold
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal="center") 
        
    #Add Dropdown Validation for PRODUCT (COLUMN C)
    dv = DataValidation(type="list", formula1="=Product_Catalog!$A$2:$A$7", allow_blank=True)
    ws_entry.add_data_validation(dv)
    dv.add:("C2:C100")
    
    #Sample starting rows + dynamic formulas down to row 100
    sample_orders = [
        [1001, "2026-11-08", "Laptop", 2],
        [1002, "2026-11-08", "Monitor", 3],
        [1003, "2026-11-08", "Headset", 5],
    ]
    for idx, order in enumerate(sample_orders, start=2):
        ws_entry[f"A{idx}"] = order[0]
        ws_entry[f"B{idx}"] = order[1]
        ws_entry[f"C{idx}"] = order[2]
        ws_entry[f"E{idx}"] = order[3]
        
    for r in range(2, 101):
        ws_entry[f"D{r}"] = f'=IF(C{r}="","",VLOOKUP(C{r},Product_Catalog!$A$2:$C$7,2,FALSE))'
        ws_entry[f"F{r}"] = f'=IF(C{r}="","",VLOOKUP(C{r},Product_Catalog!$A$2:$C$7,3,FALSE))'
        ws_entry[f"G{r}"] = f'=IF(OR(E{r}="",F{r}=""),0,E{r}*F{r})'
        ws_entry[f"F{r}"].number_format = "$#,##0.00"
        ws_entry[f"G{r}"].number_format = "$#,##0.00"
        
    #for conditional:Highlight high-value orders(> $1,000) in green
    green_fill = PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid")
    green_font = Font(color="006100", bold=True)
    ws_entry.conditional_formatting.add(
        "G2:G100",
        CellIsRule(operator="greaterThan", formula=["1000"], fill=green_fill, font=green_font),
        
    )
    
    #Tab 3: Dashboard(dynamic SUMIFS / COUNTIFS and Native Chart)
    ws_dash = wb.create_sheet(title="dashboard", index=0)
    ws_dash["A1"] = "EXECUTIVE SALES DASHBOARD"
    ws_dash["A1"].font = title_font
    
    ws_dash["A3"] = "Total Revenue"
    ws_dash["B3"] = "=SUM(Sales_Entry!G2:G100)"
    ws_dash["B3"].number_format = "$#,##0.00"
    
    ws_dash["A4"] = "Total Units Sold"
    ws_dash["B4"] = "=SUM(Sales_Entry!E2:E100)"
    ws_dash["B4"].number_format = "#,##0"
    
    ws_dash["A5"] = "Total Orders"
    ws_dash["B5"] = '=COUNTIF(Sales_Entry!C2:C100,"<>")'
    
    for r in range(3,6):
        ws_dash[f"A{r}"].font = bold_font
        ws_dash[f"A{r}"].fill = accent_fill
        ws_dash[f"B{r}"].font = bold_font
        ws_dash[f"A{r}"].border = thin_border
        ws_dash[f"B{r}"].border = thin_border
        
    ws_dash["A8"] = "Product"
    ws_dash["B8"] = "Ordes"
    ws_dash["C8"] = "Units Sold"
    ws_dash["D8"] = "Total Revenue"
    for cell in ws_dash[8]:
        cell.font = white_bold
        cell.fill = header_fill
        
    for i,item in enumerate(catalog_items, start=9):
        prod_name = item[0]
        ws_dash[f"A{i}"] = prod_name
        ws_dash[f"B{i}"] = f'=COUNTIF(Sales_Entry!$C$2:$C$100, A{i})'
        ws_dash[f"C{i}"] = f'=SUMIF(Sales_Entry!$C$2:$C$100, A{i}, Sales_Entry!$E$2:$E$100)'
        ws_dash[f"D{i}"] = f'=SUMIF(Sales_Entry!$C$2:$C$100, A{i}, Sales_Entry!$G$2:$G$100)'
        ws_dash[f"D{i}"].number_format = "$#,##0.00"
        
    #Native Excel Bar Chart
    chart = BarChart()
    chart.type = "col"
    chart.style = 10
    chart.title = "Revenue by Product"
    chart.y_axis.title = "Revenue ($)"
    chart.x_axis.title = "Product"
    data_ref = Reference(ws_dash, min_col=4, min_row=8, max_row=14)
    cats_ref = Reference(ws_dash, min_col=1, min_row=9, max_row=14)
    chart.add_data(data_ref, titles_from_data=True)
    chart.set_categories(cats_ref)
    chart.legend = None
    ws_dash.add_chart(chart, "F3")
    
    
    #Auto-adjust columns widths across all sheets
    for sheet in wb.worksheets:
        for col in sheet.columns:
            max_len = max(len(str(cell.value or "")) for cell in col)
            sheet.column_dimensions[col[0].column_letter].width=max(max_len + 4, 14)
            
    wb.save(filename)
    print(f"Advanced Excel workbook generated: {filename}")
    
if __name__ == "__main__":
    build_advanced_workbook()
        
    