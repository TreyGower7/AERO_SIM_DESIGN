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
f_x_exp = [0.3395, 0.592, 0.963]
f_y_exp = [-0.0075, -0.007, -0.0075]
f_z_exp= [-0.2285, -0.172, 0.356]
f_x_sim = [0.0011235,0.0010259,0.0010004]

f_y_sim = [0.0001545,0.0001951,0.0003089]

f_z_sim = [0.0020967,0.0022836,0.0025342]

c_x_sim = [2.22996, 2.03488, 1.987642] #x coefficient values from sims 

c_y_sim = [0.306662, 0.386972, 0.613066]

c_z_sim = [4.15788, 4.52838, 5.02712]

c_x_real = [2.655993399, 2.340258551, 1.929529931] #from our wind tunel

c_y_real = [-0.074320876, -0.035578255, -0.019034823]

c_z_real = [-1.72502664, -0.648314869, 0.729334262]


# Constants for metadata
reference_info = (
    "Reference area = 1.008e-03 m2; Density = 1.16 kg/m3; \n"
    "# Dynamic viscosity = 1.84e-05 Pa-s; Characteristic length = 3.175e-02 m"
)


# Function to write a file
def write_file(filename, header, u, re, qinf, exp_coeff, sim_coeff,f_exp,f_sim):
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
            # Write row of data
            f.write(
                f"{u[i]:.6e} {re[i]:.6e} {qinf[i]:.6e} {f_exp[i]:.6e} {exp_coeff[i]:.6e} {f_sim[i]:.6e} {sim_coeff[i]:.6e}\n"
            )

# Headers for each file
header_cx = "# C_x Data\n"
header_cy = "# C_y Data\n"
header_cz = "# C_z Data\n"

# Write files for Cx, Cy, Cz
write_file("Cx.txt", header_cx, u_sim, re_sim, qinf_sim, c_x_real, c_x_sim,f_x_exp,f_x_sim)
write_file("Cy.txt", header_cy, u_sim, re_sim, qinf_sim, c_y_real, c_y_sim, f_y_exp,f_y_sim)
write_file("Cz.txt", header_cz, u_sim, re_sim, qinf_sim, c_z_real, c_z_sim, f_z_exp,f_z_sim)
