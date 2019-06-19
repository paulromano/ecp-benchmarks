#!/usr/bin/env python3

import argparse
import copy
from pathlib import Path

import numpy as np
from tqdm import tqdm

import openmc
from smr.materials import materials
from smr.surfaces import surfs, lattice_pitch, bottom_fuel_stack, top_active_core
from smr.assemblies import assembly_universes
from smr.plots import assembly_plots


# Define command-line options
parser = argparse.ArgumentParser()
parser.add_argument('-m', '--multipole', action='store_true',
                    help='Whether to use multipole cross sections')
parser.add_argument('-t', '--tallies', choices=('cell', 'mat'), default='mat',
                    help='Whether to use distribmats or distribcells for tallies')
parser.add_argument('-r', '--rings', type=int, default=10,
                    help='Number of annular regions in fuel')
parser.add_argument('-a', '--axial', type=int, default=196,
                    help='Number of axial subdivisions in fuel')
parser.add_argument('-d', '--depleted', action='store_true',
                    help='Whether UO2 compositions should represent depleted fuel')
parser.add_argument('-o', '--output-dir', type=Path, default=None)
args = parser.parse_args()

# Make directory for inputs
if args.output_dir is None:
    if args.depleted:
        directory = Path('assembly-depleted')
    else:
        directory = Path('assembly-fresh')
else:
    directory = args.output_dir
directory.mkdir(exist_ok=True)

# Define geometry with a single assembly
assembly = assembly_universes(args.rings, args.axial, args.depleted)
lattice_sides = openmc.model.get_rectangular_prism(lattice_pitch, lattice_pitch,
                                                   boundary_type='reflective')
main_cell = openmc.Cell(
    fill=assembly['Assembly (3.1%) 16BA'],
    region=lattice_sides & +surfs['lower bound'] & -surfs['upper bound']
)
root_univ = openmc.Universe(cells=[main_cell])
geometry = openmc.Geometry(root_univ)


def clone(material):
    """Perform copy of material but share nuclide densities"""
    shared_mat = copy.copy(material)
    shared_mat.id = None
    return shared_mat


#### "Differentiate" the geometry if using distribmats
if args.tallies == 'mat':
    # Count the number of instances for each cell and material
    geometry.determine_paths(instances_only=True)

    # Extract all cells filled by a fuel material
    fuel_mats = {m for m in materials if 'UO2 Fuel' in m.name}

    for cell in tqdm(geometry.get_all_material_cells().values(),
                     desc='Differentiating materials'):
        if cell.fill in fuel_mats:
            # Fill cell with list of "differentiated" materials
            cell.fill = [clone(cell.fill) for i in range(cell.num_instances)]

#### Create OpenMC "materials.xml" file
print('Getting materials...')
all_materials = geometry.get_all_materials()
print('Creating materials collection...')
materials = openmc.Materials(all_materials.values())
print('Exporting materials to XML...')
materials.export_to_xml(str(directory / 'materials.xml'))


#### Create OpenMC "geometry.xml" file
geometry.export_to_xml(str(directory / 'geometry.xml'))


#### Create OpenMC "settings.xml" file

# Construct uniform initial source distribution over fissionable zones
lower_left = (-lattice_pitch/2, -lattice_pitch/2, bottom_fuel_stack)
upper_right = (lattice_pitch/2, lattice_pitch/2, top_active_core)
source = openmc.source.Source(space=openmc.stats.Box(lower_left, upper_right))
source.space.only_fissionable = True

settings = openmc.Settings()
settings.batches = 200
settings.inactive = 100
settings.particles = 10000
settings.output = {'tallies': False, 'summary': False}
settings.source = source
settings.sourcepoint_write = False

if args.multipole:
    settings.temperature = {'multipole': True, 'tolerance': 1000}

settings.export_to_xml(str(directory / 'settings.xml'))


####  Create OpenMC "tallies.xml" file
tallies = openmc.Tallies()

# Extract all fuel materials
materials = geometry.get_materials_by_name(name='Fuel', matching=False)

# If using distribcells, create distribcell tally needed for depletion
if args.tallies == 'cell':
    # Extract all cells filled by a fuel material
    fuel_cells = []
    for cell in geometry.get_all_cells().values():
        if cell.fill in materials:
            tally = openmc.Tally(name='depletion tally')
            tally.scores = ['(n,p)', '(n,a)', '(n,gamma)',
                            'fission', '(n,2n)', '(n,3n)', '(n,4n)']
            tally.nuclides = cell.fill.get_nuclides()
            tally.filters.append(openmc.DistribcellFilter([cell]))
            tallies.append(tally)

# If using distribmats, create material tally needed for depletion
elif args.tallies == 'mat':
    tally = openmc.Tally(name='depletion tally')
    tally.scores = ['(n,p)', '(n,a)', '(n,gamma)',
                    'fission', '(n,2n)', '(n,3n)', '(n,4n)']
    tally.nuclides = materials[0].get_nuclides()
    tally.filters = [openmc.MaterialFilter(materials)]
    tallies.append(tally)

tallies.export_to_xml(str(directory / 'tallies.xml'))

# Create plots
plots = assembly_plots(main_cell.fill)
plots.export_to_xml(str(directory / 'plots.xml'))