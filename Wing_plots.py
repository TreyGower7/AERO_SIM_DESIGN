import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def get_data():
    xls = pd.ExcelFile("https://github.com/TreyGower7/AERO_SIM_DESIGN/blob/main/wing/Aerodynamic_Testing_Wing.xlsx")
    AOAN2 = pd.read_excel(xls, 'Wing - AOA - -2.5')
    AOA0 = pd.read_excel(xls, 'Wing - AOA - 0')
    AOA2 = pd.read_excel(xls, 'Wing - AOA - 2.5')
    AOA5 = pd.read_excel(xls, 'Wing - AOA - 5')
    AOA10 = pd.read_excel(xls, 'Wing - AOA - 10')
    AOA12 = pd.read_excel(xls, 'Wing - AOA - 15')

    return [AOAN2, AOA0, AOA2, AOA5,AOA10,AOA12]


def main():
    df = get_data()
    print(df[0])

if __name__ == "main":
    main()