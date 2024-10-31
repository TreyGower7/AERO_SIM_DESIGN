import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#def get_data():
xls = pd.ExcelFile("/Users/treygower/Library/CloudStorage/OneDrive-TheUniversityofTexasatAustin/Aerodynamic_Testing_Wing.xlsx")
AOAN2 = pd.read_excel(xls, 'Wing - AOA - -2.5')
AOA0 = pd.read_excel(xls, 'Wing - AOA - 0')
AOA2 = pd.read_excel(xls, 'Wing - AOA - 2.5')
AOA5 = pd.read_excel(xls, 'Wing - AOA - 5')
AOA10 = pd.read_excel(xls, 'Wing - AOA - 10')
AOA12 = pd.read_excel(xls, 'Wing - AOA - 12.5')
df = [AOAN2, AOA0, AOA2, AOA5,AOA10,AOA12]
keyword = 'Unnamed'

# Remove columns containing the keyword
for i in range(len(df)):
 df[i] = df[i].drop(columns=[col for col in df[i].columns if keyword in col])
print(df[3].keys())

#def main():
   # df = get_data()

#if __name__ == "main":
   # main()