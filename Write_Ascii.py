import pandas as pd
from datetime import datetime
import os


# Function to calculate coefficients
def calculate_coefficient(F, q, is_moment=False):
    if is_moment:
        return F / (q * S * L)
    else:
        return F / (q * S)
    
# Define the file path for the input data
filepath = '/Users/treygower/Library/CloudStorage/OneDrive-TheUniversityofTexasatAustin/Aerodynamic_Testing_Wing.xlsx'

# Read the input data into DataFrames
xls = pd.ExcelFile(filepath)

# Labeling for loops below
aoa_sheets = {
    -2.5: pd.read_excel(xls, 'Wing - AOA - -2.5'),
    0: pd.read_excel(xls, 'Wing - AOA - 0'),
    2.5: pd.read_excel(xls, 'Wing - AOA - 2.5'),
    5: pd.read_excel(xls, 'Wing - AOA - 5'),
    10: pd.read_excel(xls, 'Wing - AOA - 10'),
    12.5: pd.read_excel(xls, 'Wing - AOA - 12.5')
}

# Define constants
S = 4.032250e-03  # Reference area in m^2
L = 3.175000e-02  # Characteristic length in m
Vapor_sat = aoa_sheets[0]["Value"][0] # Vapor Saturation
rho = aoa_sheets[0]["Value"][1] # Air density in kg/m^3
mu = aoa_sheets[0]["Value"][2] # Dynamic viscosity in Pa-s
nu = aoa_sheets[0]["Value"][3] # Kinematic viscosity in Pa-s


# Generate current date and directory information
current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
output_dir = "./AERO_SIM_DESIGN/wing/data_ascii/"  # Ensure this directory exists

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Define the coefficient names and their corresponding output file names
coefficients = {
    'Cx': 'Cx.txt',
    'Cy': 'Cy.txt',
    'Cz': 'Cz.txt',
    'Cm_x': 'Cm_x.txt',
    'Cm_y': 'Cm_y.txt',
    'Cm_z': 'Cm_z.txt'
}

# Prepare to write the ASCII files
for coeff_name, force_name in coefficients.items():
    with open(os.path.join(output_dir, f"{coeff_name}.txt"), 'w') as f:
        # Write the header with metadata
        f.write(f"# username: treygower\n")
        f.write(f"# date: {current_date}\n")
        f.write(f"# host: ase-a14261-lt.lan\n")
        f.write(f"# dir: {output_dir}\n")
        f.write("#\n")
        f.write(f"# Reference area = {S:.6e} m2; Density = 1.177212e+00 kg/m3; Dynamic viscosity = 1.909558e-05 Pa-s; Characteristic length = {L:.6e} m\n")
        f.write("#\n")
        f.write("# (1) U (m/s); (2) Re; (3) qinf (Pa); ")
        for i, aoa in enumerate(aoa_sheets.keys()):
            f.write(f"({4+i*2}) {force_name} (N), {aoa} deg; ({5+i*2}) {coeff_name}, {aoa} deg; ")
        f.write("\n")

        # Write the data rows
        for u in aoa_sheets[-2.5]['U (m/s)'].unique():
            row_data = []
            for aoa, df in aoa_sheets.items():
                row = df[df['U (m/s)'] == u].iloc[0]
                if not row_data:
                    row_data.extend([
                        f"{row['U (m/s)']:.6e}",
                        f"{row['Re']:.6e}",
                        f"{row['qinf (Pa)']:.6e}"
                    ])
                force = row[force_name]
                q = row['qinf (Pa)']
                is_moment = force_name.startswith('M')
                coeff = calculate_coefficient(force, q, is_moment)
                row_data.extend([f"{force:.6e}", f"{coeff:.6e}"])
            f.write(' '.join(row_data) + '\n')

print(f"Data files have been written to {output_dir}")