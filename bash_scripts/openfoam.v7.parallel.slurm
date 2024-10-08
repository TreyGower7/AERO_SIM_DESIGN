#!/bin/bash
#----------------------------------------------------
# Sample Slurm job script
#   for TACC Stampede2 KNL nodes
#
#   *** MPI Job on Normal Queue ***
# 
# Last revised: 20 Oct 2017
#
# Notes:
#
#   -- Launch this script by executing
#      "sbatch knl.mpi.slurm" on Stampede2 login node.
#
#   -- Use ibrun to launch MPI codes on TACC systems.
#      Do not use mpirun or mpiexec.
#
#   -- Max recommended MPI tasks per KNL node: 64-68
#      (start small, increase gradually).
#
#   -- If you're running out of memory, try running
#      fewer tasks per node to give each task more memory.
#
#----------------------------------------------------

#SBATCH -J ofparal            # Job name
#SBATCH -o job.o%j       # Name of stdout output file
#SBATCH -e job.e%j       # Name of stderr error file

### #SBATCH -p normal          # Queue (partition) name
#SBATCH -p development          # Queue (partition) name
### #SBATCH -p skx-normal          # Queue (partition) name

#SBATCH -N 1               # Total # of nodes
#SBATCH -n 8               # Total # of mpi tasks
#SBATCH -t 01:00:00        # Run time (hh:mm:ss)

### #SBATCH --mail-user=youremail@utexas.edu
### #SBATCH --mail-type=all    # Send email at begin and end of job

#SBATCH -A ECS24015       # Allocation name (req'd if you have more than 1)

# Other commands must follow all #SBATCH directives...

module purge
module load intel/19.1.1  impi/19.0.9 openfoam/7.0
module list

pwd
date

./AllrunParallel

date
