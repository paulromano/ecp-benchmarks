"""Creates a 2D 2x2 assembly colorset with a water reflector."""

import numpy as np

import opencg
import openmc
import openmc.opencg_compatible as opencg_compatible
from beavrs.builder import BEAVRS


def find_assembly(assembly_name, wrap_geometry=True):
    """Find a fuel assembly with some string name in the BEAVRS OpenCG model.

    This method extracts the fuel assembly and wraps it in an OpenCG Geometry.
    The returned geometry has reflective boundary conditions along all
    boundaries. The z-axis is bounded between z=200 and z=210 cm.

    Parameters
    ----------
    assembly_name : str
        The name of the fuel assembly lattice
    wrap_geometry : bool
        If false, the fuel assembly Lattice is returned. If true, the fuel
        assembly Lattice is wrapped in an OpenCG Geometry and returned (default).

    Returns
    -------
    fuel_assembly
        The OpenCG Lattice or Geometry for the assembly or None if not found

    """

    # Get all OpenCG Universes
    all_univ = beavrs.main_universe.get_all_universes()

    # Iterate over all Universes
    fuel_assembly = None
    for univ_id, univ in all_univ.items():
        if univ.name == assembly_name:
            fuel_assembly = univ

    # Wrap lattice in a Geometry if requested by the user
    if wrap_geometry:

        # Create a root Cell
        root_cell = opencg.Cell(name='root cell')
        root_cell.fill = fuel_assembly

        # Make mixed reflective / vacuum boundaries
        min_x = opencg.XPlane(x0=root_cell.fill.min_x, boundary='reflective')
        max_x = opencg.XPlane(x0=root_cell.fill.max_x, boundary='reflective')
        min_y = opencg.YPlane(y0=root_cell.fill.min_y, boundary='reflective')
        max_y = opencg.YPlane(y0=root_cell.fill.max_y, boundary='reflective')
        max_z = opencg.ZPlane(z0=197.5, boundary='reflective')
        min_z = opencg.ZPlane(z0=192.5, boundary='reflective')

        # Add boundaries to the root Cell
        root_cell.add_surface(surface=min_x, halfspace=+1)
        root_cell.add_surface(surface=max_x, halfspace=-1)
        root_cell.add_surface(surface=min_y, halfspace=+1)
        root_cell.add_surface(surface=max_y, halfspace=-1)
        root_cell.add_surface(surface=min_z, halfspace=+1)
        root_cell.add_surface(surface=max_z, halfspace=-1)

        # Create a root Universe
        root_univ = opencg.Universe(universe_id=0, name='root universe')
        root_univ.add_cell(root_cell)

        # Create a Geometry
        fuel_assembly = opencg.Geometry()
        fuel_assembly.root_universe = root_univ

    return fuel_assembly


def build_reflector(assembly1_name, assembly2_name):
    """Build a 2x2 fuel assembly geometry with a water reflector on the
    bottom and right.

    This routine puts reflective boundary conditions along min x, max y and z
    and vacuum boundary conditions along the max x and min y boundaries.

    Parameters
    ----------
    assembly1_name : str
        The BEAVRS fuel assembly to place in the bottom right and top left
    assembly2_name : str
        The BEAVRS fuel assembly to place in the bottom left and top right

    Returns
    -------
    opencg.Geometry
        A 2x2 fuel assembly and reflector OpenCG Geometry

    """

    fuel_assembly1 = find_assembly(assembly1_name, wrap_geometry=False)
    fuel_assembly2 = find_assembly(assembly2_name, wrap_geometry=False)

    # Find the water material
    all_cells = beavrs.main_universe.get_all_cells()
    for cell_uuid, cell in all_cells.items():
        if cell.type == 'material' and cell.fill.name == 'water':
            water = cell.fill

    # Create a Cell/Universe around the first fuel assembly
    fuel_cell1 = opencg.Cell(name='assm1 cell')
    fuel_cell1.fill = fuel_assembly1
    fuel_univ1 = opencg.Universe(name='assm1 universe')
    fuel_univ1.add_cell(fuel_cell1)

    # Create a Cell/Universe around the second fuel assembly
    fuel_cell2 = opencg.Cell(name='assm2 cell')
    fuel_cell2.fill = fuel_assembly2
    fuel_univ2 = opencg.Universe(name='assm2 universe')
    fuel_univ2.add_cell(fuel_cell2)

    # Create a Cell/Universe with water
    water_cell = opencg.Cell(name='water cell', fill=water)
    water_univ = opencg.Universe(name='water universe')
    water_univ.add_cell(water_cell)

    # Create a 3x3 lattice two fuel assemblies surrounded by a water reflector
    reflector_lattice = opencg.Lattice(name='reflector')
    lat_width = fuel_assembly1.max_x - fuel_assembly1.min_x
    reflector_lattice.width = [lat_width, lat_width, 1000.]
    reflector_lattice.dimension = [3, 3, 1]
    reflector_lattice.offset = [0., 0., 0.]
    reflector_lattice.universes = [[fuel_univ1, fuel_univ2, water_univ],
                                   [fuel_univ2, fuel_univ1, water_univ],
                                   [water_univ, water_univ, water_univ]]

    # Create a Geometry around the reflected lattice
    root_cell = opencg.Cell(name='root cell')
    root_cell.fill = reflector_lattice

    # Make mixed reflective / vacuum boundaries
    min_x = opencg.XPlane(x0=root_cell.fill.min_x, boundary='reflective')
    max_x = opencg.XPlane(x0=root_cell.fill.max_x, boundary='vacuum')
    min_y = opencg.YPlane(y0=root_cell.fill.min_y, boundary='vacuum')
    max_y = opencg.YPlane(y0=root_cell.fill.max_y, boundary='reflective')
    min_z = opencg.ZPlane(z0=192.5, boundary='reflective')
    max_z = opencg.ZPlane(z0=197.5, boundary='reflective')

    # Add boundaries to the root Cell
    root_cell.add_surface(surface=min_x, halfspace=+1)
    root_cell.add_surface(surface=max_x, halfspace=-1)
    root_cell.add_surface(surface=min_y, halfspace=+1)
    root_cell.add_surface(surface=max_y, halfspace=-1)
    root_cell.add_surface(surface=min_z, halfspace=+1)
    root_cell.add_surface(surface=max_z, halfspace=-1)

    # Create a root Universe for this fuel assembly
    root_univ = opencg.Universe(universe_id=0, name='root universe')
    root_univ.add_cell(root_cell)

    # Create an OpenCG Geometry for this fuel assembly
    reflector = opencg.Geometry()
    reflector.root_universe = root_univ

    return reflector


#### Create OpenMC "materials.xml" and "geometry.xml" files

# Instantiate a BEAVRS object
beavrs = BEAVRS(nndc_xs=True)

# Write all BEAVRS materials to materials.xml file
beavrs.write_openmc_materials()

# Extract fuel assemblies of interest from BEAVRS model
reflector = build_reflector('Fuel 1.6% enr instr no BAs',
                            'Fuel 3.1% enr instr 20')
openmc_geometry = opencg_compatible.get_openmc_geometry(reflector)
openmc_geometry.export_to_xml()


#### Create OpenMC "settings.xml" file

# Construct uniform initial source distribution over fissionable zones
lower_left = reflector.bounds[:3]
upper_right = reflector.bounds[3:]

lat_width = (np.array(upper_right) - np.array(lower_left))
lat_width[:2] /= 3.

source = openmc.source.Source(space=openmc.stats.Box(lower_left, upper_right))
source.space.only_fissionable = True

settings_file = openmc.Settings()
settings_file.batches = 100
settings_file.inactive = 10
settings_file.particles = 100000
settings_file.ptables = True
settings_file.output = {'tallies': False}
settings_file.source = source
settings_file.sourcepoint_write = False
settings_file.export_to_xml()


#### Create OpenMC MGXS libraries

# Get all cells filled with a "fuel" material
mat_cells = openmc_geometry.get_all_material_cells()
fuel_cells = []
for cell in mat_cells:
    if 'fuel' in cell.fill.name.lower():
        fuel_cells.append(cell)

# CASMO 70-group structure
energy_groups = openmc.mgxs.EnergyGroups()
energy_groups.group_edges = np.array([
    0, 0.005, 0.01, 0.015, 0.02, 0.025, 0.03, 0.035, 0.042, 0.05, 0.058, 0.067,
    0.08, 0.1, 0.14, 0.18, 0.22, 0.25, 0.28, 0.3, 0.32, 0.35, 0.4, 0.5, 0.625,
    0.78, 0.85, 0.91, 0.95, 0.972, 0.996, 1.02, 1.045, 1.071, 1.097, 1.123,
    1.15, 1.3, 1.5, 1.855, 2.1, 2.6, 3.3, 4., 9.877, 15.968, 27.7, 48.052,
    75.501, 148.73, 367.26001, 906.90002, 1.4251e3, 2.2395e3, 3.5191e3, 5.53e3,
    9.118e3, 15.03e3, 24.78e3, 40.85e3, 67.34e3, 111.e3, 183e3, 302.5e3, 500e3,
    821e3, 1.353e6, 2.231e6, 3.679e6, 6.0655e6, 2e7])

# Initialize a 70-group "distribcell" MGXS library
cell_mgxs_lib = openmc.mgxs.Library(openmc_geometry, by_nuclide=True)
cell_mgxs_lib.energy_groups = energy_groups
cell_mgxs_lib.mgxs_types = ['total', 'nu-fission', 'nu-scatter matrix', 'chi']
cell_mgxs_lib.domain_type = 'distribcell'
cell_mgxs_lib.domains = fuel_cells
cell_mgxs_lib.correction = None
cell_mgxs_lib.build_library()

# Initialize a 70-group "material" MGXS library
mat_mgxs_lib = openmc.mgxs.Library(openmc_geometry, by_nuclide=True)
mat_mgxs_lib.energy_groups = energy_groups
mat_mgxs_lib.mgxs_types = ['total', 'nu-fission', 'nu-scatter matrix', 'chi']
mat_mgxs_lib.domain_type = 'material'
mat_mgxs_lib.correction = None
mat_mgxs_lib.build_library()


####  Create mesh tallies for verification of pin-wise reaction rates

# Instantiate a tally Mesh
mesh = openmc.Mesh(name='assembly mesh')
mesh.type = 'regular'
mesh.dimension = [34, 34, 1]
mesh.lower_left = [lower_left[0], lower_left[1] + lat_width[1], lower_left[2]]
mesh.width = np.array(lat_width)
mesh.width[:2] /= 17.
mesh_filter = openmc.MeshFilter(mesh)

# Instantiate energy-integrated fission rate mesh Tally
fission_rates = openmc.Tally(name='fission rates')
fission_rates.filters = [mesh_filter]
fission_rates.scores = ['fission']

# Instantiate energy-wise U-238 capture rate mesh Tally
capture_rates = openmc.Tally(name='u-238 capture')
capture_rates.filters = [mesh_filter]
capture_rates.nuclides = ['U238']
capture_rates.scores = ['absorption', 'fission']


####  Create OpenMC "tallies.xml" file

# Create a "tallies.xml" file for the mesh tallies
tallies_file = openmc.Tallies([fission_rates, capture_rates])
cell_mgxs_lib.add_to_tallies_file(tallies_file, merge=True)
mat_mgxs_lib.add_to_tallies_file(tallies_file, merge=True)
tallies_file.export_to_xml()