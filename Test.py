import pandas as pd
from datetime import datetime
import os
import numpy as np

def write_data():
    for coeff_name, (column_name, filename) in coefficients.items():
        with open(os.path.join(output_dir, filename), 'w') as f:
            # Write header with metadata
            f.write(f"# username: tagower\n")
            f.write(f"# date: {current_date}\n")
            f.write(f"# dir: {os.getcwd()}\n")
            f.write("#\n")
            f.write(f"# Reference area = {S:.6e} m2; Density = {rho:.6e} kg/m3; \n# Dynamic viscosity = {mu:.6e} Pa-s; Characteristic length = {L:.6e} m\n")
            f.write("#\n")
            f.write("# (1) U (m/s); (2) Re; (3) qinf (Pa); ")
            for i, aoa in enumerate(df_keys):
                f.write(f"# ({4+i*2}) {column_name}, {aoa} deg; ({5+i*2}) {coeff_name}, {aoa} deg; ")
                if i % 5 == 0:
                    f.write("\n")
            f.write("\n")
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

def calc_Re(U):
    return U * L / nu

def calc_Qinf(U):
    return 0.5 * rho * (U ** 2)

def calc_coefficient(F, q):
    print(F)
    print(q)
    return F / (q * S)

    # Define the file path for the input data
filepath = '/Users/treygower/Library/CloudStorage/OneDrive-TheUniversityofTexasatAustin/Aerodynamic_Testing_Wing.xlsx'

df = get_data(filepath)
df = clean_data(df)

# Constants
S = 4.032250  # Reference area in m^2
L = 3.209798  # Characteristic chord length in m
rho = df[0]["Value"][1]  # Air density in kg/m^3
mu = df[0]["Value"][2]  # Dynamic viscosity in Pa-s
nu = df[0]["Value"][3]  # Kinematic viscosity in m^2/s

import numpy as np

# Mapping of indices to angles of attack
angle_map = {0: -2.5, 1: 0, 2: 2.5, 3: 5, 4: 10, 5: 12.5}

# Dictionaries to store values for each angle of attack
velocities = {}
reynolds_numbers = {}
coefficients_x = {}
coefficients_y = {}
coefficients_z = {}
moment_coefficients_x = {}
moment_coefficients_y = {}
moment_coefficients_z = {}

# Loop over each index in df for each angle of attack
for idx, angle in angle_map.items():
    # Initialize lists for the current angle
    vels = []
    Res = []
    Cf_x = []
    Cf_y = []
    Cf_z = []
    Cm_x = []
    Cm_y = []
    Cm_z = []
    # Loop over each row in the windspeed column for the current angle's dataframe
    for i in range(len(df[idx]["windspeed(m/s)"].dropna())):
        windspeed = df[idx]["windspeed(m/s)"].iloc[i]
        vels.append(windspeed)
        
        # Calculate Reynolds number
        Re = calc_Re(windspeed)
        if Re in Res:
            continue
        Res.append(Re)
        
        # Calculate dynamic pressure qinf
        qinf = calc_Qinf(windspeed)
        
        # Calculate force coefficients
        force_x = df[idx]["Fx (N)"].iloc[i]
        force_y = df[idx]["Fy (N)"].iloc[i]
        force_z = df[idx]["Fz (N)"].iloc[i]
        
        Cf_x.append(calc_coefficient(force_x, qinf))
        Cf_y.append(calc_coefficient(force_y, qinf))
        Cf_z.append(calc_coefficient(force_z, qinf))
        
        # Calculate moment coefficients
        moment_x = df[idx]["Tx (N)"].iloc[i]
        moment_y = df[idx]["Ty (N)"].iloc[i]
        moment_z = df[idx]["Tz (N)"].iloc[i]
        
        Cm_x.append(calc_coefficient(moment_x, qinf))
        Cm_y.append(calc_coefficient(moment_y, qinf))
        Cm_z.append(calc_coefficient(moment_z, qinf))
    
    # Store unique values in dictionaries by angle
    velocities[angle] = np.unique(vels)
    reynolds_numbers[angle] = np.unique(Res)
    coefficients_x[angle] = Cf_x
    coefficients_y[angle] = Cf_y
    coefficients_z[angle] = Cf_z
    moment_coefficients_x[angle] = Cm_x
    moment_coefficients_y[angle] = Cm_y
    moment_coefficients_z[angle] = Cm_z

# Print results for each angle of attack
for angle in angle_map.values():
    print(f"Angle of Attack {angle}°:")
    print("Unique Velocities:", velocities.get(angle, []))
    print("Unique Reynolds Numbers:", reynolds_numbers.get(angle, []))
    print("Force Coefficients Cf_x:", coefficients_x.get(angle, []))
    print("Force Coefficients Cf_y:", coefficients_y.get(angle, []))
    print("Force Coefficients Cf_z:", coefficients_z.get(angle, []))
    print("Moment Coefficients Cm_x:", moment_coefficients_x.get(angle, []))
    print("Moment Coefficients Cm_y:", moment_coefficients_y.get(angle, []))
    print("Moment Coefficients Cm_z:", moment_coefficients_z.get(angle, []))
    print("----------------------------------------------------")
