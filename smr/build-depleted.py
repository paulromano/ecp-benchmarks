from collections import OrderedDict
import copy
import os

import numpy as np
import openmc
import opendeplete

from smr.materials import materials
from smr.surfaces import lattice_pitch, bottom_fuel_stack, top_active_core
from smr.core import geometry


# FIXME: Automatically extract info needed to calculate burnable cell volumes
# Fuel rod geometric parameters
radius = 0.39218
height = 200.

# Count the number of instances for each cell and material
geometry.determine_paths()

# Determine the maximum material ID
max_material_id = 0
for material in geometry.get_all_materials().values():
    max_material_id = max(max_material_id, material.id)

# Extract all cells filled by a fuel material
fuel_cells = geometry.get_cells_by_name(
    name='(1.6%) (0)', case_sensitive=True)
fuel_cells.extend(geometry.get_cells_by_name(
    name='(1.6%) grid (bottom) (0)', case_sensitive=True))
fuel_cells.extend(geometry.get_cells_by_name(
    name='(1.6%) grid (intermediate) (0)', case_sensitive=True))
fuel_cells.extend(geometry.get_cells_by_name(
    name='(2.4%) (0)', case_sensitive=True))
fuel_cells.extend(geometry.get_cells_by_name(
    name='(2.4%) grid (bottom) (0)', case_sensitive=True))
fuel_cells.extend(geometry.get_cells_by_name(
    name='(2.4%) grid (intermediate) (0)', case_sensitive=True))
fuel_cells.extend(geometry.get_cells_by_name(
    name='(3.1%) (0)', case_sensitive=True))
fuel_cells.extend(geometry.get_cells_by_name(
    name='(3.1%) grid (bottom) (0)', case_sensitive=True))
fuel_cells.extend(geometry.get_cells_by_name(
    name='(3.1%) grid (intermediate) (0)', case_sensitive=True))

# Assign distribmats for each material
for cell in fuel_cells:
    new_materials = []

    for i in range(cell.num_instances):
        new_material = copy.deepcopy(cell.fill)
        new_material.id = max_material_id + 1
        max_material_id += 1
        new_materials.append(new_material)

        # Store volume of burnable fuel rods cells
        new_material.volume = np.pi * radius**2 * height
        new_material.depletable = True
        new_material.temperature = 300

    cell.fill = new_materials

# Create dt vector for 1 month with 5 day timesteps
dt1 = 5*24*60*60  # 5 days
dt2 = 1.*30*24*60*60  # 1 months
N = np.floor(dt2/dt1)
dt = np.repeat([dt1], N)

# Create settings variable
settings = opendeplete.OpenMCSettings()
settings.openmc_call = ["mpirun", "openmc"]
settings.particles = 1000000
settings.batches = 200
settings.inactive = 100
settings.lower_left = \
    [-7.*lattice_pitch/2., -7.*lattice_pitch/2., bottom_fuel_stack]
settings.upper_right = \
    [+7.*lattice_pitch/2., +7.*lattice_pitch/2., top_active_core]
settings.entropy_dimension = [15, 15, 1]

# MeV/second cm from CASMO
settings.power = 2.337e15 * ((17.*17.*37.) / 1.5**2) * height
settings.dt_vec = dt
settings.output_dir = 'depleted'

op = opendeplete.OpenMCOperator(geometry, settings)

# Perform simulation using the MCNPX/MCNP6 algorithm
opendeplete.integrate(op, opendeplete.ce_cm_c1)