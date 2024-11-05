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

# Constants
S = 4.032250  # Reference area in m^2
L = 3.209798  # Characteristic chord length in m
rho = aoa_sheets[0]["Value"][1]  # Air density in kg/m^3
mu = aoa_sheets[0]["Value"][2]  # Dynamic viscosity in Pa-s
nu = aoa_sheets[0]["Value"][3]  # Kinematic viscosity in m^2/s

def calc_Re(U):
    return U * L / nu

def calc_Qinf(U):
    return 0.5 * rho * (U ** 2)

def calc_coefficient(F, q):
    return F / (q * S)

username = "tagower"
date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
directory = "/Users/treygower/AERO_SIM_DESIGN"
output_folder = os.path.join(directory, "output_files")
os.makedirs(output_folder, exist_ok=True)

# Define coefficient types and their corresponding force/moment columns
coefficient_data = {
    'Cf_x': {'column': 'Fx (N)', 'description': 'Force coefficient x'},
    'Cf_y': {'column': 'Fy (N)', 'description': 'Force coefficient y'},
    'Cf_z': {'column': 'Fz (N)', 'description': 'Force coefficient z'},
    'Cm_x': {'column': 'Tx (N)', 'description': 'Moment coefficient x'},
    'Cm_y': {'column': 'Ty (N)', 'description': 'Moment coefficient y'},
    'Cm_z': {'column': 'Tz (N)', 'description': 'Moment coefficient z'}
}

def get_all_unique_velocities():
    all_velocities = set()
    for sheet in aoa_sheets.values():
        velocities = sheet['windspeed(m/s)'].dropna().unique()
        all_velocities.update(velocities)
    return sorted(list(all_velocities))

def generate_coefficient_file(coeff_name, force_column):
    output_lines = []
    
    # Header
    output_lines.extend([
        f"# username: {username}",
        f"# date: {date}",
        f"# dir: {directory}",
        "#",
        f"# Reference area = {S:e} m2; Density = {rho:e} kg/m3;",
        f"# Dynamic viscosity = {mu:e} Pa-s; Characteristic length = {L:e} m",
        "#"
    ])
    
    # Column headers
    header = "# (1) U (m/s); (2) Re; (3) qinf (Pa);"
    col_num = 4
    for aoa in [-2.5, 0, 2.5, 5, 10, 12.5]:
        header += f" # ({col_num}) {force_column}, {aoa} deg; ({col_num+1}) {coeff_name}, {aoa} deg;"
        col_num += 2
    output_lines.append(header)
    output_lines.append("")
    
    # Data rows
    velocities = get_all_unique_velocities()
    for v in velocities:
        re = calc_Re(v)
        qinf = calc_Qinf(v)
        row = [f"{v:e}", f"{re:e}", f"{qinf:e}"]
        
        for aoa in [-2.5, 0, 2.5, 5, 10, 12.5]:
            sheet = aoa_sheets[aoa]
            data = sheet[sheet['windspeed(m/s)'] == v]
            if not data.empty:
                force = data[force_column].iloc[0]
                coeff = calc_coefficient(force, qinf)
                row.extend([f"{force:e}", f"{coeff:e}"])
            else:
                row.extend(["", ""])
        
        output_lines.append(" ".join(row))
    
    # Write to file
    output_file = os.path.join(output_folder, f"{coeff_name}_data.txt")
    with open(output_file, 'w') as f:
        f.write('\n'.join(output_lines))
    
    print(f"Generated {coeff_name} file: {output_file}")
    return output_lines

# Generate files for each coefficient type
for coeff_name, data in coefficient_data.items():
    output_lines = generate_coefficient_file(coeff_name, data['column'])
    
    # Print first few lines of each file to verify format
    print(f"\nFirst few lines of {coeff_name}_data.txt:")
    for line in output_lines[:8]:
        print(line)
    print("...\n")

# Check for duplicate Reynolds numbers
velocities = get_all_unique_velocities()
reynolds_dict = {}
duplicate_re = []

for v in velocities:
    re = calc_Re(v)
    if re in reynolds_dict:
        duplicate_re.append((v, reynolds_dict[re], re))
    reynolds_dict[re] = v

if duplicate_re:
    print("\nWarning: Duplicate Reynolds numbers found:")
    print("Velocity 1 | Velocity 2 | Reynolds Number")
    for v1, v2, re in duplicate_re:
        print(f"{v1:e} | {v2:e} | {re:e}")