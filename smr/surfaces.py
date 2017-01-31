import copy
import math

import openmc

# FIXME: Add back parameters for pin cell radial surfaces
# FIXME: Cleanup parameters
# FIXME: Add docstring explanation


# Notation
# GT: Guide Tube
# BA: Burnable Absorber
# CP: Control Poison
# FR: Fuel Rod
# IR: Inner Radius
# OR: Outer Radius
# IT: Instrument Tube
# FA: Fuel Assembly
# RPV: Reactor Pressure Vessel

# Parameters
rod_grid_side_tb  = 1.24416
rod_grid_side_i   = 1.21962

## lattice parameters
pin_pitch         = 1.25984
lattice_pitch     = 21.50364
grid_strap_side   = 21.47270

## radial paramters
core_barrel_IR    = 85.0
core_barrel_OR    = 90.0
neutron_shield_OR = 92.0
baffle_width      = 2.2225
rpv_IR            = 120.0
rpv_OR            = 135.0

## axial paramters
lowest_extent        =      0.000  #
highest_extent       =    255.444  # arbitrary amount of water above core
bottom_support_plate =     20.000  # arbitrary amount of water below core
top_support_plate    =     25.000  # guessed
bottomLowerNozzle    =     25.000  # same as topSupportPlate
topLowerNozzle       =     35.160  # approx from seabrook NDR of 4.088in for lower nozzle height
bottom_fuel_rod      =     35.160  # same as topLowerNozzle
topLowerThimble      =     36.007  # approx as 1/3 of inch, this is exact seabrook NDR value for bottom thimble
bottom_fuel_stack    =     36.007  # same as topLowerThimble
activeCoreHeight     =    182.880  # provided by D***
top_active_core      =    218.887  # bottomFuelStack + activeCoreHeight
bot_burn_abs         =     41.087  # approx from seabrook NDR of 1.987in for space between bot of BAs and bot of active fuel

# grid z planes (heights 1.65 top/bottom, 2.25 intermediate)
grid1_center          =     39.974  # bottomFuelStack + 1.562in
grid1_bot             =     37.879  # grid1Center - 1.65/2
grid1_top             =     42.070  # grid1Center + 1.65/2
grid2_center          =    102.021  # bottomFuelStack + 25.990in
grid2_bot             =     99.164  # grid2Center - 2.25/2
grid2_top             =    104.879  # grid2Center + 2.25/2
grid3_center          =    154.218  # bottomFuelStack + 46.540in
grid3_bot             =    151.361  # grid3Center - 2.25/2
grid3_top             =    157.076  # grid3Center + 2.25/2
grid4_center          =    206.415  # bottomFuelStack + 67.090in
grid4_bot             =    203.558  # grid4Center - 2.25/2
grid4_top             =    209.273  # grid4Center + 2.25/2

# control rod step heights
step0H               =     45.079  # chosen to match the step size calculated for intervals between other grids
step36H              =    102.021  # grid2Center
step69H              =    154.218  # grid3Center
step102H             =    206.415  # grid4Center
step228H             =    249.122  # set using calculated step width (27*stepWidth + step102H)
step_width            =    1.58173  # calculated from grid center planes

bank_bot  = 405.713
bank_step = 228
bank_top  = 766.348

top_fuel_rod        =    223.272
top_plenum          =    221.223
bottom_upper_nozzle =    226.617
top_upper_nozzle    =    235.444

neutron_shield_NWbot_SEtop = math.tan(math.pi/3)
neutron_shield_NWtop_SEbot = math.tan(math.pi/6)
neutron_shield_NEbot_SWtop = math.tan(-math.pi/3)
neutron_shield_NEtop_SWbot = math.tan(-math.pi/6)


surfs = {}

# FIXME: Is this a good idea???
surfs['dummy outer'] = openmc.Sphere(
    x0=0., y0=0., R=4000., name='Dummy Outer Surface')


surfs['pellet OR'] = openmc.ZCylinder(
    x0=0., y0=0., R=0.39218, name='Pellet OR')
surfs['plenum spring OR'] = openmc.ZCylinder(
    x0=0., y0=0., R=0.06459, name='FR Plenum Spring OR')
surfs['clad IR'] = openmc.ZCylinder(
    x0=0., y0=0., R=0.40005, name='Clad IR')
surfs['clad OR'] = openmc.ZCylinder(
    x0=0., y0=0., R=0.45720, name='Clad OR')
surfs['GT IR'] = openmc.ZCylinder(
    x0=0., y0=0., R=0.56134, name='GT IR (above dashpot)')
surfs['GT OR'] = openmc.ZCylinder(
    x0=0., y0=0., R=0.60198, name='GT OR (above dashpot)')
surfs['GT dashpot IR'] = openmc.ZCylinder(
    x0=0., y0=0., R=0.50419, name='GT IR (at dashpot)')
surfs['GT dashpot OR'] = openmc.ZCylinder(
    x0=0., y0=0., R=0.54610, name='GT OR (at dashpot)')
surfs['CP OR'] = openmc.ZCylinder(
    x0=0., y0=0., R=0.43310, name='Control Poison OR')
surfs['CR IR'] = openmc.ZCylinder(
    x0=0., y0=0., R=0.43688, name='CR Clad IR')
surfs['CR OR'] = openmc.ZCylinder(
    x0=0., y0=0., R=0.48387, name='CR Clad OR')
surfs['BA IR 1'] = openmc.ZCylinder(
    x0=0., y0=0., R=0.21400, name='BA IR 1')
surfs['BA IR 2'] = openmc.ZCylinder(
    x0=0., y0=0., R=0.23051, name='BA IR 2')
surfs['BA IR 3'] = openmc.ZCylinder(
    x0=0., y0=0., R=0.24130, name='BA IR 3')
surfs['BA IR 4'] = openmc.ZCylinder(
    x0=0., y0=0., R=0.42672, name='BA IR 4')
surfs['BA IR 5'] = openmc.ZCylinder(
    x0=0., y0=0., R=0.43688, name='BA IR 5')
surfs['BA IR 6'] = openmc.ZCylinder(
    x0=0., y0=0., R=0.48387, name='BA IR 6')
surfs['BA IR 7'] = openmc.ZCylinder(
    x0=0., y0=0., R=0.56134, name='BA IR 7')
surfs['BA IR 8'] = openmc.ZCylinder(
    x0=0., y0=0., R=0.60198, name='BA IR 8')
surfs['IT IR'] = copy.deepcopy(surfs['BA IR 5'])
surfs['IT OR'] = copy.deepcopy(surfs['BA IR 6'])

# Planes
surfs['rod grid box xtop tb'] = openmc.XPlane(
    x0=rod_grid_side_tb/2., name='X max for grid outside FR in top/bottom spacers')
surfs['rod grid box xbot tb'] = openmc.XPlane(
    x0=-rod_grid_side_tb/2., name='X min for grid outside FR in top/bottom spacers')
surfs['rod grid box ytop tb'] = openmc.YPlane(
    y0=rod_grid_side_tb/2., name='Y max for grid outside FR in top/bottom spacers')
surfs['rod grid box ybot tb'] = openmc.YPlane(
    y0=-rod_grid_side_tb/2., name='Y min for grid outside FR in top/bottom spacers')

surfs['rod grid box xtop i'] = openmc.XPlane(
    x0=rod_grid_side_i/2, name='X max for grid outside FR in intermediate spacers')
surfs['rod grid box xbot i'] = openmc.XPlane(
    x0=-rod_grid_side_i/2, name='X min for grid outside FR in intermediate spacers')
surfs['rod grid box ytop i'] = openmc.yPlane(
    y0=rod_grid_side_i/2, name='Y max for grid outside FR in intermediate spacers')
surfs['rod grid box ybot i'] = openmc.YPlane(
    y0=-rod_grid_side_i/2, name='Y min for grid outside FR in intermediate spacers')

surfs['lat grid box xtop'] = openmc.XPlane(
    x0=grid_strap_side/2, name='X max for grid outside FA')
surfs['lat grid box xbot'] = openmc.XPlane(
    x0=-grid_strap_side/2, name='Y min for grid outside FA')
surfs['lat grid box ytop'] = openmc.YPlane(
    y0=grid_strap_side/2, name='Y max for grid outside FA')
surfs['lat grid box xbot'] = openmc.YPlane(
    y0=-grid_strap_side/2, name='Y min for grid outside FA')

surfs['lat box xtop'] = openmc.XPlane(
    x0=17.*pin_pitch/2., name='lattice X max')
surfs['lat box xbot'] = openmc.XPlane(
    x0=-17.*pin_pitch/2., name='lattice X min')
surfs['lat box ytop'] = openmc.YPlane(
    x0=17.*pin_pitch/2., name='lattice Y max')
surfs['lat box ybot'] = openmc.YPlane(
    x0=-17.*pin_pitch/2., name='lattice Y min')

surfs['lowest extent'] = openmc.ZPlane(
    z0=lowest_extent, name='lowest extent')
surfs['bot support plate'] = openmc.ZPlane(
    z0=bottom_support_plate, name='bot support plate')
surfs['top support plate'] = openmc.ZPlane(
    z0=top_support_plate, name='top support plate')
surfs['bot fuel rod'] = openmc.ZPlane(z0=bottom_fuel_rod, name='bottom FR')
surfs['top lower nozzle'] = copy.deepcopy(surfs['bottom FR'])
surfs['bot lower nozzle'] = copy.deepcopy(surfs['top support plate'])

# axial surfaces
surfs['bot active core'] = openmc.ZPlane(
    z0=bottom_fuel_stack, name='bot active core')
surfs['top active core'] = openmc.ZPlane(
    z0=top_active_core, name='top active core')

surfs['top lower thimble'] = copy.deepcopy(surfs['bot active core'])
surfs['burn abs bot'] = openmc.ZPlane(
    z0=bot_burn_abs, name='bottom of BA')

surfs['grid1bot'] = openmc.ZPlane(
    z0=grid1_bot, name='bottom grid 1')
surfs['grid1top'] = openmc.ZPlane(
    z0=grid1_top, name='top of grid 1')
surfs['dashpot top'] = openmc.ZPlane(
    z0=step0H, name='top dashpot')
surfs['grid2bot'] = openmc.ZPlane(
    z0=grid2_bot, name='bottom grid 2')
surfs['grid2top'] = openmc.ZPlane(
    z0=grid2_top, name='top grid 2')
surfs['grid3bot'] = openmc.ZPlane(
    z0=grid3_bot, name='bottom of grid 3')
surfs['grid3top'] = openmc.ZPlane(
    z0=grid3_top, name='top of grid 3')
surfs['grid4bot'] = openmc.ZPlane(
    z0=grid4_bot, name='bottom of grid 4')
surfs['grid4top'] = openmc.ZPlane(
    z0=grid4_top, name='top grid 4')

grid_surfaces = [surfs['grid1bot']['id'],
                 surfs['grid1top']['id'],
                 surfs['grid2bot']['id'],
                 surfs['grid2top']['id'],
                 surfs['grid3bot']['id'],
                 surfs['grid3top']['id'],
                 surfs['grid4bot']['id'],
                 surfs['grid4top']['id']]

surfs['top pin plenum'] = openmc.ZPlane(
    z0=top_plenum, name='top pin plenum')
surfs['top fuel rod'] = openmc.ZPlane(
    z0=top_fuel_rod, name='top fuel rod')
surfs['bot upper nozzle'] = openmc.ZPlane(
    z0=bottom_upper_nozzle, name='bottom upper nozzle')
surfs['top upper nozzle'] = openmc.ZPlane(
    z0=top_upper_nozzle, name='top upper nozzle')
surfs['highest extent'] = openmc.ZPlane(
    z0=highest_extent, name='highest extent')

# Control rod bank surfaces for ARO configuration
for bank in ['A','B','C','D','E',]:
    surfs['bank{} top'.format(bank)] = openmc.ZPlane(
        z0=step228H+step_width*228, name='CR bank {} top'.format(bank))
    surfs['bank{} top'.format(bank)] = openmc.ZPlane(
        z0=step228H, name='CR bank {} bottom'.format(bank))

surfs['bankA top'] = openmc.ZPlane(
    z0=bank_top, name='CR bank A top')
surfs['bankA bot'] = openmc.ZPlane(
    z0=bank_bot, name='CR bank A bottom')
surfs['bankB top'] = openmc.ZPlane(
    z0=bank_top, name='CR bank B top')
surfs['bankB bot'] = openmc.ZPlane(
    z0=bank_bot, name='CR bank B bottom')
surfs['bankC top'] = openmc.ZPlane(
    z0=bank_top, name='CR bank C top')
surfs['bankC bot'] = openmc.ZPlane(
    z0=bank_bot, name='CR bank C bottom')
surfs['bankD top'] = openmc.ZPlane(
    z0=bank_top, name='CR bank D top')
surfs['bankD bot'] = openmc.ZPlane(
    z0=bank_bot, name='CR bank D bottom')

# outer radial surfaces
surfs['core barrel IR'] = openmc.ZCylinder(
    x0=0., y0=0., R=core_barrel_IR, name='core barrel IR')
surfs['core barrel OR'] = openmc.ZCylinder(
    x0=0., y0=0., R=core_barrel_OR, name='core barrel OR')
surfs['neutron shield OR'] = openmc.ZPlane(
    x0=0., y0=0., R=neutron_shield_OR, name='neutron shield OR')

# neutron shield planes
surfs['neutron shield NWbot SEtop'] = openmc.Plane(
    A=1., B=neutron_shield_NWbot_SEtop, C=0., D=0.,
    name='neutron shield NWbot SEtop')
surfs['neutron shield NWtop SEbot'] = openmc.Plane(
    A=1., B=neutron_shield_NWtop_SEbot, C=0., D=0.,
    name='neutron shield NWtop SEbot')
surfs['neutron shield NEbot SWtop'] = openmc.Plane(
    A=1., B=neutron_shield_NEbot_SWtop, C=0., D=0.,
    name='neutron shield NEbot SWtop')
surfs['neutron shield NEtop SWbot'] = openmc.Plane(
    A=1., B=neutron_shield_NEtop_SWbot, C=0., D=0.,
    name='neutron shield NEtop SWbot')

# outer radial surfaces
surfs['RPV IR'] = openmc.ZCylinder(
    x0=0., y0=0., R=rpv_IR, name='RPV IR')
surfs['RPV OR'] = openmc.ZCylinder(
    x0=0., y0=0., R=rpv_OR, name='RPV OR')

# outer axial surfaces
surfs['upper bound'] = openmc.ZPlane(
    z0=highest_extent, name='upper problem boundary')
surfs['lower bound'] = openmc.ZPlane(
    z0=lowest_extent, name='lower problem boundary')