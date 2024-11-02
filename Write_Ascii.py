import pandas as pd
from datetime import datetime
import os
import numpy as np

# Define the file path for the input data
filepath = '/Users/treygower/Library/CloudStorage/OneDrive-TheUniversityofTexasatAustin/Aerodynamic_Testing_Wing.xlsx'

# Read the input data into DataFrames
xls = pd.ExcelFile(filepath)

# Load angle of attack (AOA) sheets into a dictionary
aoa_sheets = {
    -2.5: pd.read_excel(xls, 'Wing - AOA - -2.5'),
    0: pd.read_excel(xls, 'Wing - AOA - 0'),
    2.5: pd.read_excel(xls, 'Wing - AOA - 2.5'),
    5: pd.read_excel(xls, 'Wing - AOA - 5'),
    10: pd.read_excel(xls, 'Wing - AOA - 10'),
    12.5: pd.read_excel(xls, 'Wing - AOA - 12.5')
}

# Define constants
S = 4.032250  # Reference area in m^2
L = 3.175000  # Characteristic length in m
rho = aoa_sheets[0]["Value"][1] # Air density in kg/m^3
mu = aoa_sheets[0]["Value"][2] # Dynamic viscosity in Pa-s
nu = aoa_sheets[0]["Value"][3] # Kinematic viscosity in m^2/s

# Function to calculate coefficients
def calculate_coefficient(F, q, is_moment=False):
    return F / (q * S * L if is_moment else q * S)

# Function to calculate Reynolds number and dynamic pressure
def calculate_Re_Qinf(U, is_Re=False):
    return U * L / nu if is_Re else 0.5 * rho * (U ** 2)

# Generate current date and define output directory
current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
output_dir = "./wing/data_ascii"
os.makedirs(output_dir, exist_ok=True)

# Coefficient mappings with corresponding force/moment columns and output file names
coefficients = {
    'Cx': ('Fx (N)', 'Cx.txt'),
    'Cy': ('Fy (N)', 'Cy.txt'),
    'Cz': ('Fz (N)', 'Cz.txt'),
    'Cm_x': ('Tx (N)', 'Cm_x.txt'),
    'Cm_y': ('Ty (N)', 'Cm_y.txt'),
    'Cm_z': ('Tz (N)', 'Cm_z.txt')
}

# Writing ASCII files with data for each coefficient
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
        for i, aoa in enumerate(aoa_sheets.keys()):
            f.write(f"# ({4+i*2}) {column_name}, {aoa} deg; ({5+i*2}) {coeff_name}, {aoa} deg; ")
            if i % 5 == 0:
                f.write("\n")
        f.write("\n")

        unique_reynolds = set()
        # Write data rows
        for u in aoa_sheets[0]['windspeed(m/s)'].unique():
            row_data = []
            Re = calculate_Re_Qinf(u, is_Re=True)
                # Check if the Reynolds number has already been recorded
            if Re in unique_reynolds:
                continue
            unique_reynolds.add(Re)  # Add the new Reynolds number to the set
            if u != 0:
                for aoa, df in aoa_sheets.items():
                    row = df[df['windspeed(m/s)'].round(6) == round(u, 6)].iloc[:1]
                    if row.empty:
                        continue

                    windspeed = row['windspeed(m/s)'].iloc[0]
                    
                    q_inf = calculate_Re_Qinf(windspeed, is_Re=False)

                    if not row_data:
                        row_data.extend([
                            f"{windspeed:.6e}",
                            f"{Re:.6e}",
                            f"{q_inf:.6e}"
                        ])
                    
                    force = row[column_name].iloc[0]
                    is_moment = column_name.startswith('T')
                    coeff = calculate_coefficient(force, q_inf, is_moment)
                    row_data.extend([f"{force:.6e}", f"{coeff:.6e}"])
                
                f.write(' '.join(row_data) + '\n')