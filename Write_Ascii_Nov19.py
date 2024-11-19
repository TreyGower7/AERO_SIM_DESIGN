import os
import datetime

# Metadata
username = "tagower"
date = datetime.datetime.now().strftime("%a %b %d %H:%M:%S %Z %Y")
host = os.uname().nodename
directory = os.getcwd()

# Change this data to our experiments
u_sim = [1.0, 1.0, 1.0]  # Velocity (m/s)
re_sim = [29615, 41674, 58629]  # Reynolds numbers
qinf_sim = [58.86061, 88.29092, 117.72122]  # Dynamic pressure (Pa)

# Coefficients
c_x_sim = [0.5594, 0.5087, 0.4803]
c_y_sim = [0, 0, 0]
c_z_sim = [1.006, 1.1089, 1.1885]

c_x_real = [2.66, 2.35, 1.93]
c_y_real = [-0.0588, -0.0278, -0.0150]
c_z_real = [-1.79, -0.684, 0.713]

# Constants for metadata
reference_info = (
    "Reference area = 1.008e-03 m2; Density = 1.16 kg/m3; \n"
    "# Dynamic viscosity = 1.84e-05 Pa-s; Characteristic length = 3.175e-02 m"
)


# Function to write a file
def write_file(filename, header, u, re, qinf, exp_coeff, sim_coeff):
    with open(filename, "w") as f:
        # Write metadata
        f.write(f"# username: {username}\n")
        f.write(f"# date: {date}\n")
        f.write(f"# host: {host}\n")
        f.write(f"# dir: {directory}\n")
        f.write("#\n")
        f.write(f"# {reference_info}\n")
        f.write("#\n")
        f.write(
            "# (1) U (m/s); (2) Re; (3) qinf (Pa); (4) experiment-Fx (N), 0 deg;\n"
            "# (5) experiment-Cx (-); (6) simulations-Fx (N), 0 deg;\n"
            "# (7) simulations-Cx (-)\n"
        )
        # Write the data
        for i in range(len(re)):
            # Calculate experimental and simulation forces
            exp_fx = exp_coeff[i] * qinf[i]  # Experiment force
            sim_fx = sim_coeff[i] * qinf[i]  # Simulation force
            # Write row of data
            f.write(
                f"{u[i]:.6e} {re[i]:.6e} {qinf[i]:.6e} {exp_fx:.6e} {exp_coeff[i]:.6e} {sim_fx:.6e} {sim_coeff[i]:.6e}\n"
            )

# Headers for each file
header_cx = "# C_x Data\n"
header_cy = "# C_y Data\n"
header_cz = "# C_z Data\n"

# Write files for Cx, Cy, Cz
write_file("Cx.txt", header_cx, u_sim, re_sim, qinf_sim, c_x_real, c_x_sim)
write_file("Cy.txt", header_cy, u_sim, re_sim, qinf_sim, c_y_real, c_y_sim)
write_file("Cz.txt", header_cz, u_sim, re_sim, qinf_sim, c_z_real, c_z_sim)
