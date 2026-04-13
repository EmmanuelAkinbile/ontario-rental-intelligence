import os
import shutil
from datetime import datetime

folder = r"C:\Users\emman\OneDrive\Documents\ontario-rental-market-intelligence"
today = datetime.today().strftime('%Y-%m-%d')
source = os.path.join(folder, f"kijiji_rentals_clean_{today}.csv")
destination = os.path.join(folder, "kijiji_rentals_clean_latest.csv")

if os.path.exists(source):
    shutil.copy2(source, destination)
    print(f"Updated kijiji_rentals_clean_latest.csv from {source}")
else:
    print(f"ERROR: {source} not found")