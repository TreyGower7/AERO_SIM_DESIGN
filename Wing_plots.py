import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def get_data(filepath):
    # Load the Excel file and each sheet into separate DataFrames
    xls = pd.ExcelFile(filepath)
    AOAN2 = pd.read_excel(xls, 'Wing - AOA - -2.5')
    AOA0 = pd.read_excel(xls, 'Wing - AOA - 0')
    AOA2 = pd.read_excel(xls, 'Wing - AOA - 2.5')
    AOA5 = pd.read_excel(xls, 'Wing - AOA - 5')
    AOA10 = pd.read_excel(xls, 'Wing - AOA - 10')
    AOA12 = pd.read_excel(xls, 'Wing - AOA - 12.5')
    return [AOAN2, AOA0, AOA2, AOA5, AOA10, AOA12]

def clean_data(dataframes, keyword='Unnamed'):
    # Remove columns containing the specified keyword
    cleaned_data = []
    for df in dataframes:
        cleaned_df = df.drop(columns=[col for col in df.columns if keyword in col])
        cleaned_data.append(cleaned_df)
    return cleaned_data

def main():
    filepath = '/Users/treygower/Library/CloudStorage/OneDrive-TheUniversityofTexasatAustin/Aerodynamic_Testing_Wing.xlsx'
    
    # Load and clean the data
    dataframes = get_data(filepath)
    cleaned_dataframes = clean_data(dataframes)

    # Verify columns of the cleaned dataframe
    print(cleaned_dataframes[-1].columns)
    print(cleaned_dataframes[0]['Fy (N)'])

if __name__ == "__main__":
    main()
