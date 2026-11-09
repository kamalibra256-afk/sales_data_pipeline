import subprocess
import sys
from activity_logger import log_activity

def run_script(script_name):
    print(f'\n--- Running {script_name}')
    result = subprocess.run([sys.executable, script_name])
    if result.returncode != 0:
        print(f"Error encountered while running {script_name}.")
        
def main():
    while True:
        print("\n=== Sales pipeline control centre ===")
        print("1. Generate New Mock Data (main.py)")
        print("2. Run Product Revenue Analysis (analyzer.py)")
        print("3. Run Monthly Trends Analysis (trends.py)")
        print("4. Export Cleaned Data CSV (exporter.py)")
        print("5. Display Revenue Bar Charts (charts.py)")
        print("6. Run Automated Unit Tests (test_analyzer.py)")
        print("7. Exit")
        
        choice = input("select an option (1-5): ").strip()
        if choice == "1":
            run_script("main.py")
        elif choice == "2":
            run_script("analyzer.py")
        elif choice == "3":
            run_script("trends.py")
        elif choice == "4":
            subprocess.run([sys.executable, "m", "unittest", "test_analyzer.py", "-v"])
        elif choice == "5":
            log_activity("System Logout: Closed the control centre session via option 5.")
            print("Existing Sales Pipeline.")
            break
        else:
            print("Invalid selection. Enter a number from 1 to 5")
            
if __name__ == "__main__":
    main()