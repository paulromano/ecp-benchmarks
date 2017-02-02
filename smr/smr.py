#!/usr/bin/env python

"""
PWR OpenMC Model Generator

Allows for tweaking of specifications for the PWR OpenMC model, producing:
  geometry.xml
  materials.xml
  settings.xml
  plot.xml
  tallies.xml

"""

from __future__ import division

from templates2 import *

############## Geometry paramters ##############

def init_data():
  """All model parameters set here

  Materials, surfaces, cells, and lattices are defined here and automatically written
  to the proper files later.  Dictionary keys need to match those in the templates.

  The order each item is written is the order of appearance as written below

  Notes about core construction:
    The entire axial extent for each pincell is constructed in universes, and then added to fuel assembly lattices
    The fuel assembly lattices are then added to one master core lattice


  """


  ################## lattices ##################

  assemblyCells = {} # convenience dictionary holds which cells point to which assembly type

  # commonly needed universes
  gtu = cells['GT empty stack']['univ']
  gti = cells['GT empty stack instr']['univ']
  bas = cells['burn abs stack']['univ']
  ins = cells['GT instr stack']['univ']
  crA = cells['GT CR bank A']['univ']
  crB = cells['GT CR bank B']['univ']
  crC = cells['GT CR bank C']['univ']
  crD = cells['GT CR bank D']['univ']
  crSA = cells['GT CR bank SA']['univ']
  crSB = cells['GT CR bank SB']['univ']
  crSC = cells['GT CR bank SC']['univ']
  crSD = cells['GT CR bank SD']['univ']
  crSE = cells['GT CR bank SE']['univ']

  latDims = { 'dim':17, 'lleft':-17*pinPitch/2, 'width':pinPitch}

  ## 1.6 w/o assemblies

  for cent,comment1 in [(gti,""),(ins," + instr")]:

    if cent == gti:
      sss = "Core Lattice universes"
    else:
      sss = None

    # No BAs
    newCells = make_assembly(latts, cells, surfs, lo, co, univIDs, cellIDs, mats['water-nominal']['id'],
                  'Fuel 1.6 w/o'+comment1,comm="Assembly 1.6 w/o no BAs"+comment1, sect=sss,
                                 univs=pinLattice_t.format(cells['Fuel 1.6 w/o stack']['univ'],
                                                    a=gtu,  b=gtu,  c=gtu,
                                            d=gtu,                          e=gtu,
                                            f=gtu,  g=gtu,  h=gtu,  i=gtu,  j=gtu,
                                            k=gtu,  l=gtu,  m=cent, n=gtu,  o=gtu,
                                            p=gtu,  q=gtu,  r=gtu,  s=gtu,  t=gtu,
                                            u=gtu,                          v=gtu,
                                                    w=gtu,  x=gtu,  y=gtu,),
                                 gridSurfs=gridSurfaces, sleeveMats=[mats['SS304']['id'],mats['zirc']['id']],
                                 **latDims)
    assemblyCells['Fuel 1.6 w/o'+comment1] = newCells

    for bank,comment2 in [(crA,' + CRA'),(crB,' + CRB'),(crC,' + CRC'),(crD,' + CRD'),
                          (crSB,' + shutB'),(crSC,' + shutC'),(crSD,' + shutD'),(crSE,' + shutE')]:

      newCells = make_assembly(latts, cells, surfs, lo, co, univIDs, cellIDs, mats['water-nominal']['id'],
                    'Fuel 1.6 w/o'+comment1+comment2,comm="Assembly 1.6 w/o"+comment1+comment2,
                                   univs=pinLattice_t.format(cells['Fuel 1.6 w/o stack']['univ'],
                                                      a=bank,  b=bank,  c=bank,
                                              d=bank,                             e=bank,
                                              f=bank,  g=bank,  h=bank,  i=bank,  j=bank,
                                              k=bank,  l=bank,  m=cent,  n=bank,  o=bank,
                                              p=bank,  q=bank,  r=bank,  s=bank,  t=bank,
                                              u=bank,                             v=bank,
                                                      w=bank,  x=bank,  y=bank,),
                                 gridSurfs=gridSurfaces, sleeveMats=[mats['SS304']['id'],mats['zirc']['id']],
                                 **latDims)
      assemblyCells['Fuel 1.6 w/o'+comment1+comment2] = newCells



  ## 2.4 w/o assemblies

  for cen,comment1 in [(gti,""),(ins," + instr")]:

    # no BAs
    bank = gtu
    newCells = make_assembly(latts, cells, surfs, lo, co, univIDs, cellIDs, mats['water-nominal']['id'],
                  'Fuel 2.4 w/o'+comment1,comm="Assembly 2.4 w/o no BAs"+comment1,
                                 univs=pinLattice_t.format(cells['Fuel 2.4 w/o stack']['univ'],
                                                    a=bank,  b=bank,  c=bank,
                                            d=bank,                             e=bank,
                                            f=bank,  g=bank,  h=bank,  i=bank,  j=bank,
                                            k=bank,  l=bank,  m=cen,   n=bank,  o=bank,
                                            p=bank,  q=bank,  r=bank,  s=bank,  t=bank,
                                            u=bank,                             v=bank,
                                                    w=bank,  x=bank,  y=bank,),
                                 gridSurfs=gridSurfaces, sleeveMats=[mats['SS304']['id'],mats['zirc']['id']],
                                 **latDims)
    assemblyCells['Fuel 2.4 w/o'+comment1] = newCells

    # CRD
    bank = crD
    comment2 = ' + CRD'
    newCells = make_assembly(latts, cells, surfs, lo, co, univIDs, cellIDs, mats['water-nominal']['id'],
                  'Fuel 2.4 w/o'+comment1+comment2,comm="Assembly 2.4 w/o "+comment1+comment2,
                                 univs=pinLattice_t.format(cells['Fuel 2.4 w/o stack']['univ'],
                                                    a=bank,  b=bank,  c=bank,
                                            d=bank,                             e=bank,
                                            f=bank,  g=bank,  h=bank,  i=bank,  j=bank,
                                            k=bank,  l=bank,  m=cen,   n=bank,  o=bank,
                                            p=bank,  q=bank,  r=bank,  s=bank,  t=bank,
                                            u=bank,                             v=bank,
                                                    w=bank,  x=bank,  y=bank,),
                                 gridSurfs=gridSurfaces, sleeveMats=[mats['SS304']['id'],mats['zirc']['id']],
                                 **latDims)
    assemblyCells['Fuel 2.4 w/o'+comment1+comment2] = newCells

    # 12 BAs
    comment2 = ' + 12BA'
    newCells = make_assembly(latts, cells, surfs, lo, co, univIDs, cellIDs, mats['water-nominal']['id'],
                  'Fuel 2.4 w/o'+comment1+comment2,comm="Assembly 2.4 w/o"+comment1+comment2,
                                 univs=pinLattice_t.format(cells['Fuel 2.4 w/o stack']['univ'],
                                                    a=bas,  b=gtu,  c=bas,
                                            d=bas,                          e=bas,
                                            f=bas,  g=gtu,  h=gtu,  i=gtu,  j=bas,
                                            k=gtu,  l=gtu,  m=cen,  n=gtu,  o=gtu,
                                            p=bas,  q=gtu,  r=gtu,  s=gtu,  t=bas,
                                            u=bas,                          v=bas,
                                                    w=bas,  x=gtu,  y=bas,),
                                 gridSurfs=gridSurfaces, sleeveMats=[mats['SS304']['id'],mats['zirc']['id']],
                                 **latDims)
    assemblyCells['Fuel 2.4 w/o'+comment1+comment2] = newCells

    # 16 BAs
    comment2 = ' + 16BA'
    newCells = make_assembly(latts, cells, surfs, lo, co, univIDs, cellIDs, mats['water-nominal']['id'],
                  'Fuel 2.4 w/o'+comment1+comment2,comm="Assembly 2.4 w/o"+comment1+comment2,
                                 univs=pinLattice_t.format(cells['Fuel 2.4 w/o stack']['univ'],
                                                    a=bas,  b=bas,  c=bas,
                                            d=bas,                          e=bas,
                                            f=bas,  g=gtu,  h=gtu,  i=gtu,  j=bas,
                                            k=bas,  l=gtu,  m=cen,  n=gtu,  o=bas,
                                            p=bas,  q=gtu,  r=gtu,  s=gtu,  t=bas,
                                            u=bas,                          v=bas,
                                                    w=bas,  x=bas,  y=bas,),
                                 gridSurfs=gridSurfaces, sleeveMats=[mats['SS304']['id'],mats['zirc']['id']],
                                 **latDims)
    assemblyCells['Fuel 2.4 w/o'+comment1+comment2] = newCells
    
  ## 3.1 w/o assemblies

  for cen,comment1 in [(gti,""),(ins," + instr")]:

    # no BAs
    bank = gtu
    newCells = make_assembly(latts, cells, surfs, lo, co, univIDs, cellIDs, mats['water-nominal']['id'],
                  'Fuel 3.1 w/o'+comment1,comm="Assembly 3.1 w/o no BAs"+comment1,
                                 univs=pinLattice_t.format(cells['Fuel 3.1 w/o stack']['univ'],
                                                    a=bank,  b=bank,  c=bank,
                                            d=bank,                             e=bank,
                                            f=bank,  g=bank,  h=bank,  i=bank,  j=bank,
                                            k=bank,  l=bank,  m=cen,   n=bank,  o=bank,
                                            p=bank,  q=bank,  r=bank,  s=bank,  t=bank,
                                            u=bank,                             v=bank,
                                                    w=bank,  x=bank,  y=bank,),
                                 gridSurfs=gridSurfaces, sleeveMats=[mats['SS304']['id'],mats['zirc']['id']],
                                 **latDims)
    assemblyCells['Fuel 3.1 w/o'+comment1] = newCells
    
    # shut
    bank = crSA
    comment2 = ' + shutA'
    newCells = make_assembly(latts, cells, surfs, lo, co, univIDs, cellIDs, mats['water-nominal']['id'],
                  'Fuel 3.1 w/o'+comment1+comment2,comm="Assembly 3.1 w/o"+comment1+comment2,
                                 univs=pinLattice_t.format(cells['Fuel 3.1 w/o stack']['univ'],
                                                    a=bank,  b=bank,  c=bank,
                                            d=bank,                             e=bank,
                                            f=bank,  g=bank,  h=bank,  i=bank,  j=bank,
                                            k=bank,  l=bank,  m=cen,   n=bank,  o=bank,
                                            p=bank,  q=bank,  r=bank,  s=bank,  t=bank,
                                            u=bank,                             v=bank,
                                                    w=bank,  x=bank,  y=bank,),
                                 gridSurfs=gridSurfaces, sleeveMats=[mats['SS304']['id'],mats['zirc']['id']],
                                 **latDims)
    assemblyCells['Fuel 3.1 w/o'+comment1+comment2] = newCells
    
    # 20 BAs
    comment2 = ' + 20BA'
    newCells = make_assembly(latts, cells, surfs, lo, co, univIDs, cellIDs, mats['water-nominal']['id'],
                  'Fuel 3.1 w/o'+comment1+comment2,comm="Assembly 3.1 w/o"+comment1+comment2,
                                 univs=pinLattice_t.format(cells['Fuel 3.1 w/o stack']['univ'],
                                                    a=bas,  b=bas,  c=bas,
                                            d=bas,                          e=bas,
                                            f=bas,  g=bas,  h=gtu,  i=bas,  j=bas,
                                            k=bas,  l=gtu,  m=cen,  n=gtu,  o=bas,
                                            p=bas,  q=bas,  r=gtu,  s=bas,  t=bas,
                                            u=bas,                          v=bas,
                                                    w=bas,  x=bas,  y=bas,),
                                 gridSurfs=gridSurfaces, sleeveMats=[mats['SS304']['id'],mats['zirc']['id']],
                                 **latDims)
    assemblyCells['Fuel 3.1 w/o'+comment1+comment2] = newCells

    # 16 BAs
    comment2 = ' + 16BA'
    newCells = make_assembly(latts, cells, surfs, lo, co, univIDs, cellIDs, mats['water-nominal']['id'],
                  'Fuel 3.1 w/o'+comment1+comment2,comm="Assembly 3.1 w/o"+comment1+comment2,
                                 univs=pinLattice_t.format(cells['Fuel 3.1 w/o stack']['univ'],
                                                    a=bas,  b=bas,  c=bas,
                                            d=bas,                          e=bas,
                                            f=bas,  g=gtu,  h=gtu,  i=gtu,  j=bas,
                                            k=bas,  l=gtu,  m=cen,  n=gtu,  o=bas,
                                            p=bas,  q=gtu,  r=gtu,  s=gtu,  t=bas,
                                            u=bas,                          v=bas,
                                                    w=bas,  x=bas,  y=bas,),
                                 gridSurfs=gridSurfaces, sleeveMats=[mats['SS304']['id'],mats['zirc']['id']],
                                 **latDims)
    assemblyCells['Fuel 3.1 w/o'+comment1+comment2] = newCells
    
    # 15 BAs NW
    comment2 = ' + 15BANW'
    newCells = make_assembly(latts, cells, surfs, lo, co, univIDs, cellIDs, mats['water-nominal']['id'],
                  'Fuel 3.1 w/o'+comment1+comment2,comm="Assembly 3.1 w/o"+comment1+comment2,
                                 univs=pinLattice_t.format(cells['Fuel 3.1 w/o stack']['univ'],
                                                    a=gtu,  b=gtu,  c=gtu,
                                            d=gtu,                          e=gtu,
                                            f=gtu,  g=bas,  h=bas,  i=bas,  j=bas,
                                            k=gtu,  l=bas,  m=cen,  n=bas,  o=bas,
                                            p=gtu,  q=bas,  r=bas,  s=bas,  t=bas,
                                            u=gtu,                          v=bas,
                                                    w=bas,  x=bas,  y=bas,),
                                 gridSurfs=gridSurfaces, sleeveMats=[mats['SS304']['id'],mats['zirc']['id']],
                                 **latDims)
    assemblyCells['Fuel 3.1 w/o'+comment1+comment2] = newCells

    # 15 BAs NE
    comment2 = ' + 15BANE'
    newCells = make_assembly(latts, cells, surfs, lo, co, univIDs, cellIDs, mats['water-nominal']['id'],
                  'Fuel 3.1 w/o'+comment1+comment2,comm="Assembly 3.1 w/o"+comment1+comment2,
                                 univs=pinLattice_t.format(cells['Fuel 3.1 w/o stack']['univ'],
                                                    a=gtu,  b=gtu,  c=gtu,
                                            d=gtu,                          e=gtu,
                                            f=bas,  g=bas,  h=bas,  i=bas,  j=gtu,
                                            k=bas,  l=bas,  m=cen,  n=bas,  o=gtu,
                                            p=bas,  q=bas,  r=bas,  s=bas,  t=gtu,
                                            u=bas,                          v=gtu,
                                                    w=bas,  x=bas,  y=bas,),
                                 gridSurfs=gridSurfaces, sleeveMats=[mats['SS304']['id'],mats['zirc']['id']],
                                 **latDims)
    assemblyCells['Fuel 3.1 w/o'+comment1+comment2] = newCells
    
    # 15 BAs SW
    comment2 = ' + 15BASW'
    newCells = make_assembly(latts, cells, surfs, lo, co, univIDs, cellIDs, mats['water-nominal']['id'],
                  'Fuel 3.1 w/o'+comment1+comment2,comm="Assembly 3.1 w/o"+comment1+comment2,
                                 univs=pinLattice_t.format(cells['Fuel 3.1 w/o stack']['univ'],
                                                    a=bas,  b=bas,  c=bas,
                                            d=gtu,                          e=bas,
                                            f=gtu,  g=bas,  h=bas,  i=bas,  j=bas,
                                            k=gtu,  l=bas,  m=cen,  n=bas,  o=bas,
                                            p=gtu,  q=bas,  r=bas,  s=bas,  t=bas,
                                            u=gtu,                          v=gtu,
                                                    w=gtu,  x=gtu,  y=gtu,),
                                 gridSurfs=gridSurfaces, sleeveMats=[mats['SS304']['id'],mats['zirc']['id']],
                                 **latDims)
    assemblyCells['Fuel 3.1 w/o'+comment1+comment2] = newCells
    
    # 15 BAs SE
    comment2 = ' + 15BASE'
    newCells = make_assembly(latts, cells, surfs, lo, co, univIDs, cellIDs, mats['water-nominal']['id'],
                  'Fuel 3.1 w/o'+comment1+comment2,comm="Assembly 3.1 w/o"+comment1+comment2,
                                 univs=pinLattice_t.format(cells['Fuel 3.1 w/o stack']['univ'],
                                                    a=bas,  b=bas,  c=bas,
                                            d=bas,                          e=gtu,
                                            f=bas,  g=bas,  h=bas,  i=bas,  j=gtu,
                                            k=bas,  l=bas,  m=cen,  n=bas,  o=gtu,
                                            p=bas,  q=bas,  r=bas,  s=bas,  t=gtu,
                                            u=gtu,                          v=gtu,
                                                    w=gtu,  x=gtu,  y=gtu,),
                                 gridSurfs=gridSurfaces, sleeveMats=[mats['SS304']['id'],mats['zirc']['id']],
                                 **latDims)
    assemblyCells['Fuel 3.1 w/o'+comment1+comment2] = newCells
    
    # 6 BAs N
    comment2 = ' + 6BAN'
    newCells = make_assembly(latts, cells, surfs, lo, co, univIDs, cellIDs, mats['water-nominal']['id'],
                  'Fuel 3.1 w/o'+comment1+comment2,comm="Assembly 3.1 w/o"+comment1+comment2,
                                 univs=pinLattice_t.format(cells['Fuel 3.1 w/o stack']['univ'],
                                                    a=gtu,  b=gtu,  c=gtu,
                                            d=gtu,                          e=gtu,
                                            f=gtu,  g=gtu,  h=gtu,  i=gtu,  j=gtu,
                                            k=gtu,  l=gtu,  m=cen,  n=gtu,  o=gtu,
                                            p=bas,  q=gtu,  r=gtu,  s=gtu,  t=bas,
                                            u=bas,                          v=bas,
                                                    w=bas,  x=gtu,  y=bas,),
                                 gridSurfs=gridSurfaces, sleeveMats=[mats['SS304']['id'],mats['zirc']['id']],
                                 **latDims)
    assemblyCells['Fuel 3.1 w/o'+comment1+comment2] = newCells
    
    # 6 BAs S
    comment2 = ' + 6BAS'
    newCells = make_assembly(latts, cells, surfs, lo, co, univIDs, cellIDs, mats['water-nominal']['id'],
                  'Fuel 3.1 w/o'+comment1+comment2,comm="Assembly 3.1 w/o"+comment1+comment2,
                                 univs=pinLattice_t.format(cells['Fuel 3.1 w/o stack']['univ'],
                                                    a=bas,  b=gtu,  c=bas,
                                            d=bas,                          e=bas,
                                            f=bas,  g=gtu,  h=gtu,  i=gtu,  j=bas,
                                            k=gtu,  l=gtu,  m=cen,  n=gtu,  o=gtu,
                                            p=gtu,  q=gtu,  r=gtu,  s=gtu,  t=gtu,
                                            u=gtu,                          v=gtu,
                                                    w=gtu,  x=gtu,  y=gtu,),
                                 gridSurfs=gridSurfaces, sleeveMats=[mats['SS304']['id'],mats['zirc']['id']],
                                 **latDims)
    assemblyCells['Fuel 3.1 w/o'+comment1+comment2] = newCells

    # 6 BAs W
    comment2 = ' + 6BAW'
    newCells = make_assembly(latts, cells, surfs, lo, co, univIDs, cellIDs, mats['water-nominal']['id'],
                  'Fuel 3.1 w/o'+comment1+comment2,comm="Assembly 3.1 w/o"+comment1+comment2,
                                 univs=pinLattice_t.format(cells['Fuel 3.1 w/o stack']['univ'],
                                                    a=gtu,  b=gtu,  c=bas,
                                            d=gtu,                          e=bas,
                                            f=gtu,  g=gtu,  h=gtu,  i=gtu,  j=bas,
                                            k=gtu,  l=gtu,  m=cen,  n=gtu,  o=gtu,
                                            p=gtu,  q=gtu,  r=gtu,  s=gtu,  t=bas,
                                            u=gtu,                          v=bas,
                                                    w=gtu,  x=gtu,  y=bas,),
                                 gridSurfs=gridSurfaces, sleeveMats=[mats['SS304']['id'],mats['zirc']['id']],
                                 **latDims)
    assemblyCells['Fuel 3.1 w/o'+comment1+comment2] = newCells
    
    # 6 BAs E
    comment2 = ' + 6BAE'
    newCells = make_assembly(latts, cells, surfs, lo, co, univIDs, cellIDs, mats['water-nominal']['id'],
                  'Fuel 3.1 w/o'+comment1+comment2,comm="Assembly 3.1 w/o"+comment1+comment2,
                                 univs=pinLattice_t.format(cells['Fuel 3.1 w/o stack']['univ'],
                                                    a=bas,  b=gtu,  c=gtu,
                                            d=bas,                          e=gtu,
                                            f=bas,  g=gtu,  h=gtu,  i=gtu,  j=gtu,
                                            k=gtu,  l=gtu,  m=cen,  n=gtu,  o=gtu,
                                            p=bas,  q=gtu,  r=gtu,  s=gtu,  t=gtu,
                                            u=bas,                          v=gtu,
                                                    w=bas,  x=gtu,  y=gtu,),
                                 gridSurfs=gridSurfaces, sleeveMats=[mats['SS304']['id'],mats['zirc']['id']],
                                 **latDims)
    assemblyCells['Fuel 3.1 w/o'+comment1+comment2] = newCells

    

  ################## Main Core Lattices ##################

  latts['Main Core'] =          { 'order':   inc_order(lo),
                                  'comm':    comm_t.format("Main Core Lattice"),
                                  'id':      new_id(univIDs),
                                  'type':    'rectangular',
                                  'dim':     19,
                                  'lleft':   -19*latticePitch/2,
                                  'width':   latticePitch,
                                  'univs':   coreLattice_t.format(
dummy = cells['water pin']['univ'],

G___5 = cells['Fuel 3.1 w/o + instr lattice']['univ'],
H___5 = cells['Fuel 1.6 w/o + shutB lattice']['univ'],
J___5 = cells['Fuel 3.1 w/o + instr lattice']['univ'],
F___6 = cells['Fuel 3.1 w/o + instr lattice']['univ'],
G___6 = cells['Fuel 1.6 w/o + shutB lattice']['univ'],
H___6 = cells['Fuel 3.1 w/o + 16BA lattice']['univ'],
J___6 = cells['Fuel 1.6 w/o + shutB lattice']['univ'],
K___6 = cells['Fuel 3.1 w/o + instr lattice']['univ'],
E___7 = cells['Fuel 3.1 w/o + instr lattice']['univ'],
F___7 = cells['Fuel 1.6 w/o + shutB lattice']['univ'],
G___7 = cells['Fuel 3.1 w/o + 16BA lattice']['univ'],
H___7 = cells['Fuel 2.4 w/o + CRD lattice']['univ'],
J___7 = cells['Fuel 3.1 w/o + 16BA lattice']['univ'],
K___7 = cells['Fuel 1.6 w/o + shutB lattice']['univ'],
L___7 = cells['Fuel 3.1 w/o + instr lattice']['univ'],
E___8 = cells['Fuel 1.6 w/o + shutB lattice']['univ'],
F___8 = cells['Fuel 3.1 w/o + 16BA lattice']['univ'],
G___8 = cells['Fuel 2.4 w/o + CRD lattice']['univ'],
H___8 = cells['Fuel 1.6 w/o + instr lattice']['univ'],
J___8 = cells['Fuel 2.4 w/o + CRD lattice']['univ'],
K___8 = cells['Fuel 3.1 w/o + 16BA lattice']['univ'],
L___8 = cells['Fuel 1.6 w/o + shutB lattice']['univ'],
E___9 = cells['Fuel 3.1 w/o + instr lattice']['univ'],
F___9 = cells['Fuel 1.6 w/o + shutB lattice']['univ'],
G___9 = cells['Fuel 3.1 w/o + 16BA lattice']['univ'],
H___9 = cells['Fuel 2.4 w/o + CRD lattice']['univ'],
J___9 = cells['Fuel 3.1 w/o + 16BA lattice']['univ'],
K___9 = cells['Fuel 1.6 w/o + shutB lattice']['univ'],
L___9 = cells['Fuel 3.1 w/o + instr lattice']['univ'],
F__10 = cells['Fuel 3.1 w/o + instr lattice']['univ'],
G__10 = cells['Fuel 1.6 w/o + shutB lattice']['univ'],
H__10 = cells['Fuel 3.1 w/o + 16BA lattice']['univ'],
J__10 = cells['Fuel 1.6 w/o + shutB lattice']['univ'],
K__10 = cells['Fuel 3.1 w/o + instr lattice']['univ'],
G__11 = cells['Fuel 3.1 w/o + instr lattice']['univ'],
H__11 = cells['Fuel 1.6 w/o + shutB lattice']['univ'],
J__11 = cells['Fuel 3.1 w/o + instr lattice']['univ'],
**baffle)}


  ################## universe 0 cells ##################

  # the axial pincell universes contained in the lattices include the nozzles and bot support plate
  cells['inside core barrel'] ={ 'order':  inc_order(co),
                                'section': comm_t.format("Main universe cells"),
                                'comm':    comm_t.format("inside core barrel"),
                                'id':      new_id(cellIDs),
                                'univ':    0,
                                'fill':    latts['Main Core']['id'],
                                'surfs':  '-{0} {1} -{2}'.format(surfs['core barrel IR']['id'],
                                                                 surfs['lower bound']['id'],
                                                                 surfs['upper bound']['id'])}
  cells['core barrel'] =      { 'order':   inc_order(co),
                                'comm':    comm_t.format("core barrel"),
                                'id':      new_id(cellIDs),
                                'univ':    0,
                                'mat':     mats['SS304']['id'],
                                'fill':    None,
                                'surfs':  '{0} -{1} {2} -{3}'.format(surfs['core barrel IR']['id'],surfs['core barrel OR']['id'],
                                                                     surfs['lower bound']['id'],
                                                                     surfs['upper bound']['id'])}
                                                                     
  cells['shield panel NW'] =   { 'order':   inc_order(co),
                                'comm':    comm_t.format("neutron shield panel NW"),
                                'id':      new_id(cellIDs),
                                'univ':    0,
                                'mat':     mats['SS304']['id'],
                                'fill':    None,
                                'surfs':  '{0} -{1} {2} -{3} {4} -{5}'.format(surfs['core barrel OR']['id'],surfs['neut shield OR']['id'],
                                                                     surfs['neut shield NWbot SEtop']['id'],surfs['neut shield NWtop SEbot']['id'],
                                                                     surfs['lower bound']['id'],
                                                                     surfs['upper bound']['id'])}
  cells['shield panel N'] =   { 'order':   inc_order(co),
                                'comm':    "",
                                'id':      new_id(cellIDs),
                                'univ':    0,
                                'mat':     mats['water-nominal']['id'],
                                'fill':    None,
                                'surfs':  '{0} -{1} {2} -{3} {4} -{5}'.format(surfs['core barrel OR']['id'],surfs['neut shield OR']['id'],
                                                                     surfs['neut shield NWtop SEbot']['id'],surfs['neut shield NEtop SWbot']['id'],
                                                                     surfs['lower bound']['id'],
                                                                     surfs['upper bound']['id'])}
  cells['shield panel SE'] = { 'order':   inc_order(co),
                                'comm':    comm_t.format("neutron shield panel SE"),
                                'id':      new_id(cellIDs),
                                'univ':    0,
                                'mat':     mats['SS304']['id'],
                                'fill':    None,
                                'surfs':  '{0} -{1} -{2} {3} {4} -{5}'.format(surfs['core barrel OR']['id'],surfs['neut shield OR']['id'],
                                                                     surfs['neut shield NWbot SEtop']['id'],surfs['neut shield NWtop SEbot']['id'],
                                                                     surfs['lower bound']['id'],
                                                                     surfs['upper bound']['id'])}
  cells['shield panel E'] =   { 'order':   inc_order(co),
                                'comm':    "",
                                'id':      new_id(cellIDs),
                                'univ':    0,
                                'mat':     mats['water-nominal']['id'],
                                'fill':    None,
                                'surfs':  '{0} -{1} {2} {3} {4} -{5}'.format(surfs['core barrel OR']['id'],surfs['neut shield OR']['id'],
                                                                     surfs['neut shield NWbot SEtop']['id'],surfs['neut shield NEbot SWtop']['id'],
                                                                     surfs['lower bound']['id'],
                                                                     surfs['upper bound']['id'])}
  cells['shield panel NE'] =  { 'order':   inc_order(co),
                                'comm':    comm_t.format("neutron shield panel NE"),
                                'id':      new_id(cellIDs),
                                'univ':    0,
                                'mat':     mats['SS304']['id'],
                                'fill':    None,
                                'surfs':  '{0} -{1} {2} -{3} {4} -{5}'.format(surfs['core barrel OR']['id'],surfs['neut shield OR']['id'],
                                                                     surfs['neut shield NEbot SWtop']['id'],surfs['neut shield NEtop SWbot']['id'],
                                                                     surfs['lower bound']['id'],
                                                                     surfs['upper bound']['id'])}
  cells['shield panel S'] =   { 'order':   inc_order(co),
                                'comm':    "",
                                'id':      new_id(cellIDs),
                                'univ':    0,
                                'mat':     mats['water-nominal']['id'],
                                'fill':    None,
                                'surfs':  '{0} -{1} -{2} {3} {4} -{5}'.format(surfs['core barrel OR']['id'],surfs['neut shield OR']['id'],
                                                                     surfs['neut shield NWtop SEbot']['id'],surfs['neut shield NEtop SWbot']['id'],
                                                                     surfs['lower bound']['id'],
                                                                     surfs['upper bound']['id'])}
  cells['shield panel SW'] =  { 'order':   inc_order(co),
                                'comm':    comm_t.format("neutron shield panel SW"),
                                'id':      new_id(cellIDs),
                                'univ':    0,
                                'mat':     mats['SS304']['id'],
                                'fill':    None,
                                'surfs':  '{0} -{1} -{2} {3} {4} -{5}'.format(surfs['core barrel OR']['id'],surfs['neut shield OR']['id'],
                                                                     surfs['neut shield NEbot SWtop']['id'],surfs['neut shield NEtop SWbot']['id'],
                                                                     surfs['lower bound']['id'],
                                                                     surfs['upper bound']['id'])}
  cells['shield panel W'] =   { 'order':   inc_order(co),
                                'comm':    "",
                                'id':      new_id(cellIDs),
                                'univ':    0,
                                'mat':     mats['water-nominal']['id'],
                                'fill':    None,
                                'surfs':  '{0} -{1} -{2} -{3} {4} -{5}'.format(surfs['core barrel OR']['id'],surfs['neut shield OR']['id'],
                                                                     surfs['neut shield NWbot SEtop']['id'],surfs['neut shield NEbot SWtop']['id'],
                                                                     surfs['lower bound']['id'],
                                                                     surfs['upper bound']['id'])}                                                                     
                                                                   
                                                                     
  cells['downcomer'] =        { 'order':   inc_order(co),
                                'comm':    comm_t.format("downcomer"),
                                'id':      new_id(cellIDs),
                                'univ':    0,
                                'mat':     mats['water-nominal']['id'],
                                'fill':    None,
                                'surfs':  '{0} -{1} {2} -{3}'.format(surfs['neut shield OR']['id'],surfs['RPV IR']['id'],
                                                                     surfs['lower bound']['id'],
                                                                     surfs['upper bound']['id'])}
  cells['rpv'] =              { 'order':   inc_order(co),
                                'comm':    comm_t.format("pressure vessel"),
                                'id':      new_id(cellIDs),
                                'univ':    0,
                                'mat':     mats['carbon steel']['id'],
                                'fill':    None,
                                'surfs':  '{0} -{1} {2} -{3}'.format(surfs['RPV IR']['id'],surfs['RPV OR']['id'],
                                                                     surfs['lower bound']['id'],
                                                                     surfs['upper bound']['id'])}

  



  # plot parameters
  plots = {}
  
  colSpecMat = {  mats['water-nominal']['id']: "198 226 255",  # water:  light blue
                  mats['inconel']['id'] : "101 101 101",       # inconel dgray
                  mats['carbon steel']['id'] : "0 0 0",        # carbons black
                  mats['zirc']['id']:  "201 201 201",          # zirc:   gray
                  mats['SS304']['id']:  "0 0 0",               # ss304:  black
                  mats['air']['id']:  "255 255 255",           # air:    white
                  mats['helium']['id']:  "255 218 185",        # helium: light orange
                  mats['borosilicate']['id']: "0 255 0",       # BR:     green
                  mats['control rod']['id']: "255 0 0",        # CR:     bright red
                  mats['UO2 1.6']['id']: "142 35 35",          # 1.6:    light red
                  mats['UO2 2.4']['id']: "255 215 0",          # 2.4:    gold
                  mats['UO2 3.1']['id']: "0 0 128",            # 3.1:    dark blue
               }
  
  plots["row 8 axial"] ={ 'id':     new_id(plotIDs),
                              'fname':  'row_8_mats_axial',
                              'type':   'slice', 
                              'col':    'mat',
                              'background': '255 255 255',
                              'origin': '0.0 0.0 {0}'.format((highestExtent-lowestExtent)/2),
                              'width':  '{0} {0}'.format(highestExtent-lowestExtent),
                              'basis':  'xz',
                              'pixels': '6000 6000',
                              'spec':   colSpecMat,}
  plots["mats J8 ax bot"] = { 'id':     new_id(plotIDs),
                               'fname':  'J8_mats_ax_bot',
                               'type':   'slice', 
                               'col':    'mat',
                               'background': '255 255 255',
                               'origin': '{x} {y} {z}'.format(x=0.0,y=latticePitch,z=topLowerNozzle),
                               'width':  '{x} {z}'.format(x=latticePitch,z=2.1*(topLowerNozzle-bottomSupportPlate)),
                               'basis':  'xz',
                               'pixels': '{x} {z}'.format(x=4000,z=int(4000*2.1*(topLowerNozzle-bottomSupportPlate)/latticePitch)),
                               'spec':   colSpecMat,}
  plots["mats J8 ax top"] = { 'id':     new_id(plotIDs),
                               'fname':  'J8_mats_ax_top',
                               'type':   'slice', 
                               'col':    'mat',
                               'background': '255 255 255',
                               'origin': '{x} {y} {z}'.format(x=0.0,y=latticePitch,z=topFuelRod),
                               'width':  '{x} {z}'.format(x=latticePitch,z=2.1*(topUpperNozzle - topFuelRod)),
                               'basis':  'xz',
                               'pixels': '{x} {z}'.format(x=4000,z=int(4000*2.1*(topLowerNozzle-bottomSupportPlate)/latticePitch)),
                               'spec':   colSpecMat,}
  plots["mats J8 nozzle"] = { 'id':     new_id(plotIDs),
                               'fname':  'J8_mats_nozzle',
                               'type':   'slice',
                               'col':    'mat',
                               'background': '255 255 255',
                               'origin': '{x} {y} {z}'.format(x=0.0,y=latticePitch,z=bottomSupportPlate+2.0),
                               'width':  '{x} {y}'.format(x=latticePitch,y=latticePitch),
                               'basis':  'xy',
                               'pixels': '{x} {y}'.format(x=4000,y=4000),
                               'spec':   colSpecMat,}
  plots["mats H8 ax top"] = { 'id':     new_id(plotIDs),
                               'fname':  'H8_mats_ax_top',
                               'type':   'slice', 
                               'col':    'mat',
                               'background': '255 255 255',
                               'origin': '{x} {y} {z}'.format(x=0.0,y=0.0,z=topFuelRod),
                               'width':  '{x} {z}'.format(x=latticePitch,z=5*(topUpperNozzle - topFuelRod)),
                               'basis':  'xz',
                               'pixels': '{x} {z}'.format(x=4000,z=int(4000*2.1*(topLowerNozzle-bottomSupportPlate)/latticePitch)),
                               'spec':   colSpecMat,}


  # settings parameters
  entrX = 15*17
  entrY = 15*17
  entrZ = 100
  xbot = -8*latticePitch/2
  ybot = -8*latticePitch/2
  zbot = bottomFuelStack
  xtop = 8*latticePitch/2
  ytop = 8*latticePitch/2
  ztop = topActiveCore
  if core_D == '2-D':
    entrZ = 1
    zbot = twoDlower
    ztop = twoDhigher 
  sett = { 
            'xslib':        '/home/shared/mcnpdata/binary/cross_sections.xml',
#            'xslib':        '/home/nhorelik/xsdata/cross_sections.xml',
            'batches':      350,
            'inactive':     250,
            'particles':    int(4e4),
            'verbosity':    7,
            'entrX':        entrX, 
            'entrY':        entrY,
            'entrZ':        entrZ,
            'xbot':   xbot, 'ybot':  ybot, 'zbot': zbot,
            'xtop':   xtop, 'ytop':  ytop, 'ztop': ztop}



  tallies = {}

  meshDim = 15*17
  meshLleft = -15*latticePitch/2
  tallies['testmesh'] = {'ttype': 'mesh',
                      'id': 1,
                      'type': 'rectangular',
                      'origin': '0.0 0.0',
                      'width': '{0} {0}'.format(-meshLleft*2/meshDim),
                      'lleft': '{0} {0}'.format(meshLleft),
                      'dimension': '{0} {0}'.format(meshDim)}
  tallies['test'] = { 'ttype': 'tally',
                      'id': 1,
                      'mesh':tallies['testmesh']['id'],
                      'scores':'nu-fission'}

  return mats,surfs,cells,latts,sett,plots,tallies


def make_assembly(latts, cells, surfs, lo, co, univIDs, cellIDs, water, name,
                  comm=None,sect=None, dim=None,lleft=None,width=None,univs=None,
                  gridSurfs=None,sleeveMats=None):
  """Populates the cells and latts dictionary with an assembly

    The cell universe handle to use will be:  cells[name+' lattice']['univ']
  
    cells      - cells dictionary
    surfs      - surfs dictionary
    lo         - latts order dictionary
    co         - cells order dictionary
    univIDs    - set of already used universe IDs
    cellIDs    - set of already used cell IDs
    name       - string, name of the latt/cell family
    water      - material to put outside the lattice
    comm       - optional comment for the lattice and cell family
    sect       - optional section comment
    dim        - required lattice dimension
    lleft      - required lattice lower_left
    width      - required lattice width
    univs      - required lattice universe string.  Should be made with pinLattice_t
    gridSurfs  - required list of grid surface ids, from bottom to top
    sleeveMats - required materials for grid sleeves as [topbot,intermediate]

    returns list of all the created cell keys

  """

  name = str(name)

  # first make the lattice

  latts[name] =                 { 'order':   inc_order(lo),
                                  'id':      new_id(univIDs),
                                  'type':    'rectangular'}
  if comm:
    latts[name]['comm'] = comm_t.format(comm)
  else:
    latts[name]['comm'] = ""
  if sect:
    latts[name]['section'] = comm_t.format(sect)

  for key in ['dim','lleft','width','univs']:
    if not locals()[key]:
      raise Exception('make_assembly requires {0}'.format(key))
    else:
      latts[name][key] = locals()[key]
  
  # add lattice to bounding cell
  cells[name+' lattice'] =    { 'order':   inc_order(co),
                                'id':      new_id(cellIDs),
                                'univ':    new_id(univIDs),
                                'fill':    latts[name]['id'],
                                'surfs':  '-{0} {1} -{2} {3}'.format(surfs['lat box xtop']['id'],surfs['lat box xbot']['id'],surfs['lat box ytop']['id'],surfs['lat box ybot']['id'])}
  if comm:
    cells[name+' lattice']['comm'] = comm_t.format(comm)
  else:
    cells[name+' lattice']['comm'] = ""
  if sect:
    cells[name+' lattice']['section'] = comm_t.format(sect)
  
  
  # make axial all cells for outside of assembly

  # !! all of this would be greatly simplified if box-type surfaces were implemented in openmc !!
  
  outKeys = []  # we only keep track of this to facilitate certain plots/tallies
  
  # first bottom part
  cells[name+' lattice 2'] =  { 'order':   inc_order(co), 'comm':"",
                                'id':      new_id(cellIDs),
                                'univ':    cells[name+' lattice']['univ'],
                                'fill':    None,
                                'mat':     water,
                                'surfs':  '-{0} -{1}'.format(surfs['lat box ybot']['id'],gridSurfs[0])}
  outKeys.append(cells[name+' lattice 2']['id'])
  cells[name+' lattice 3'] =  { 'order':   inc_order(co), 'comm':"",
                                'id':      new_id(cellIDs),
                                'univ':    cells[name+' lattice']['univ'],
                                'fill':    None,
                                'mat':     water,
                                'surfs':  '{0} -{1}'.format(surfs['lat box ytop']['id'],gridSurfs[0])}
  outKeys.append(cells[name+' lattice 3']['id'])
  cells[name+' lattice 4'] =  { 'order':   inc_order(co), 'comm':"",
                                'id':      new_id(cellIDs),
                                'univ':    cells[name+' lattice']['univ'],
                                'fill':    None,
                                'mat':     water,
                                'surfs':  '{0} -{1} {2} -{3}'.format(surfs['lat box xtop']['id'],
                                                                surfs['lat box ytop']['id'],surfs['lat box ybot']['id'],
                                                                gridSurfs[0])}
  outKeys.append(cells[name+' lattice 4']['id'])
  cells[name+' lattice 5'] =  { 'order':   inc_order(co), 'comm':"",
                                'id':      new_id(cellIDs),
                                'univ':    cells[name+' lattice']['univ'],
                                'fill':    None,
                                'mat':     water,
                                'surfs':  '-{0} -{1} {2} -{3}'.format(surfs['lat box xbot']['id'],
                                                                 surfs['lat box ytop']['id'],surfs['lat box ybot']['id'],
                                                                 gridSurfs[0])}
  outKeys.append(cells[name+' lattice 5']['id'])

  gridnum = 0
  
  # all middle cells
  for i,botGridSurf in enumerate(gridSurfs[:-1]):
  
  
    if i%2 == 0:
      # make gridsleeve cells

      gridnum += 1
      
      if gridnum == 1 or gridnum == 8:
        smat = sleeveMats[0]
      else:
        smat = sleeveMats[1]
      
      outSurfsKey = 'lat grid box '
      inSurfsKey = 'lat box '
           
      cellKey = name+' lattice grid {0}'.format(6+i*4)
      cells[cellKey] =  { 'order':   inc_order(co), 'comm':"",
                          'id':      new_id(cellIDs),
                          'univ':    cells[name+' lattice']['univ'],
                          'fill':    None,
                          'mat':     smat,
                          'surfs':  '-{0} {1} {2} -{3} {4} -{5}'.format(surfs[inSurfsKey+'ybot']['id'],surfs[outSurfsKey+'ybot']['id'],
                                                                        surfs[outSurfsKey+'xbot']['id'],surfs[outSurfsKey+'xtop']['id'],
                                                                        botGridSurf,gridSurfs[i+1])}
      outKeys.append(cells[cellKey]['id'])
      cellKey = name+' lattice grid {0}'.format(7+i*4)
      cells[cellKey] =  { 'order':   inc_order(co), 'comm':"",
                          'id':      new_id(cellIDs),
                          'univ':    cells[name+' lattice']['univ'],
                          'fill':    None,
                          'mat':     smat,
                          'surfs':  '-{0} {1} {2} -{3} {4} -{5}'.format(surfs[outSurfsKey+'ytop']['id'],surfs[inSurfsKey+'ytop']['id'],
                                                                        surfs[outSurfsKey+'xbot']['id'],surfs[outSurfsKey+'xtop']['id'],
                                                                        botGridSurf,gridSurfs[i+1])}
      outKeys.append(cells[cellKey]['id'])
      cellKey = name+' lattice grid {0}'.format(8+i*4)
      cells[cellKey] =  { 'order':   inc_order(co), 'comm':"",
                          'id':      new_id(cellIDs),
                          'univ':    cells[name+' lattice']['univ'],
                          'fill':    None,
                          'mat':     smat,
                          'surfs':  '-{0} {1} {2} -{3} {4} -{5}'.format(surfs[inSurfsKey+'xbot']['id'],surfs[outSurfsKey+'xbot']['id'],
                                                                        surfs[inSurfsKey+'ybot']['id'],surfs[inSurfsKey+'ytop']['id'],
                                                                        botGridSurf,gridSurfs[i+1])}
      outKeys.append(cells[cellKey]['id'])
      cellKey = name+' lattice grid {0}'.format(9+i*4)
      cells[cellKey] =  { 'order':   inc_order(co), 'comm':"",
                          'id':      new_id(cellIDs),
                          'univ':    cells[name+' lattice']['univ'],
                          'fill':    None,
                          'mat':     smat,
                          'surfs':  '-{0} {1} {2} -{3} {4} -{5}'.format(surfs[outSurfsKey+'xtop']['id'],surfs[inSurfsKey+'xtop']['id'],
                                                                        surfs[inSurfsKey+'ybot']['id'],surfs[inSurfsKey+'ytop']['id'],
                                                                        botGridSurf,gridSurfs[i+1])}
      outKeys.append(cells[cellKey]['id'])
      
    else:
      outSurfsKey = 'lat box '
  
  
    cellKey = name+' lattice {0}'.format(6+i*4)
    cells[cellKey] =  { 'order':   inc_order(co), 'comm':"",
                        'id':      new_id(cellIDs),
                        'univ':    cells[name+' lattice']['univ'],
                        'fill':    None,
                        'mat':     water,
                        'surfs':  '-{0} {1} -{2}'.format(surfs[outSurfsKey+'ybot']['id'],botGridSurf,gridSurfs[i+1])}
    outKeys.append(cells[cellKey]['id'])
    cellKey = name+' lattice {0}'.format(7+i*4)
    cells[cellKey] =  { 'order':   inc_order(co), 'comm':"",
                        'id':      new_id(cellIDs),
                        'univ':    cells[name+' lattice']['univ'],
                        'fill':    None,
                        'mat':     water,
                        'surfs':  '{0} {1} -{2}'.format(surfs[outSurfsKey+'ytop']['id'],botGridSurf,gridSurfs[i+1])}
    outKeys.append(cells[cellKey]['id'])
    cellKey = name+' lattice {0}'.format(8+i*4)
    cells[cellKey] =  { 'order':   inc_order(co), 'comm':"",
                        'id':      new_id(cellIDs),
                        'univ':    cells[name+' lattice']['univ'],
                        'fill':    None,
                        'mat':     water,
                        'surfs':  '{0} -{1} {2} {3} -{4}'.format(surfs[outSurfsKey+'xtop']['id'],
                                                        surfs[outSurfsKey+'ytop']['id'],surfs[outSurfsKey+'ybot']['id'],
                                                        botGridSurf,gridSurfs[i+1])}
    outKeys.append(cells[cellKey]['id'])
    cellKey = name+' lattice {0}'.format(9+i*4)
    cells[cellKey] =  { 'order':   inc_order(co), 'comm':"",
                        'id':      new_id(cellIDs),
                        'univ':    cells[name+' lattice']['univ'],
                        'fill':    None,
                        'mat':     water,
                        'surfs':  '-{0} -{1} {2} {3} -{4}'.format(surfs[outSurfsKey+'xbot']['id'],
                                                         surfs[outSurfsKey+'ytop']['id'],surfs[outSurfsKey+'ybot']['id'],
                                                         botGridSurf,gridSurfs[i+1])}
    outKeys.append(cells[cellKey]['id'])
    
  # top part
  cells[name+' lat last 1'] = { 'order':   inc_order(co), 'comm':"",
                                'id':      new_id(cellIDs),
                                'univ':    cells[name+' lattice']['univ'],
                                'fill':    None,
                                'mat':     water,
                                'surfs':  '-{0} {1}'.format(surfs['lat box ybot']['id'],gridSurfs[-1])}
  outKeys.append(cells[name+' lat last 1']['id'])
  cells[name+' lat last 2'] = { 'order':   inc_order(co), 'comm':"",
                                'id':      new_id(cellIDs),
                                'univ':    cells[name+' lattice']['univ'],
                                'fill':    None,
                                'mat':     water,
                                'surfs':  '{0} {1}'.format(surfs['lat box ytop']['id'],gridSurfs[-1])}
  outKeys.append(cells[name+' lat last 2']['id'])
  cells[name+' lat last 3'] = { 'order':   inc_order(co), 'comm':"",
                                'id':      new_id(cellIDs),
                                'univ':    cells[name+' lattice']['univ'],
                                'fill':    None,
                                'mat':     water,
                                'surfs':  '{0} -{1} {2} {3}'.format(surfs['lat box xtop']['id'],
                                                                surfs['lat box ytop']['id'],surfs['lat box ybot']['id'],
                                                                gridSurfs[-1])}
  outKeys.append(cells[name+' lat last 3']['id'])
  cells[name+' lat last 4'] = { 'order':   inc_order(co), 'comm':"",
                                'id':      new_id(cellIDs),
                                'univ':    cells[name+' lattice']['univ'],
                                'fill':    None,
                                'mat':     water,
                                'surfs':  '-{0} -{1} {2} {3}'.format(surfs['lat box xbot']['id'],
                                                                 surfs['lat box ytop']['id'],surfs['lat box ybot']['id'],
                                                                 gridSurfs[-1])}
  outKeys.append(cells[name+' lat last 4']['id'])
  
  
  
  return outKeys # we only keep track of this to facilitate certain plots/tallies


def main():

  mats,surfs,cells,latts,sett,plots,tallies,cmfd = init_data()

  write_materials(mats,"materials.xml")
  write_geometry(surfs,cells,latts,"geometry.xml")
  write_settings(sett,"settings.xml")
  write_plots(plots,"plots.xml")
  write_tallies(tallies,"tallies.xml")
  write_cmfd(cmfd,"cmfd.xml")


if __name__ == "__main__":
  main()
