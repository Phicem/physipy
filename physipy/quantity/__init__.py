# !/usr/bin/env python
# -*- coding: utf-8 -*-

from .quantity import Dimension, Quantity
from .quantity import DimensionError, SI_UNIT_SYMBOL
from .quantity import quantify, make_quantity, dimensionify
from .utils import check_dimension, set_favunit, dimension_and_favunit, drop_dimension, add_back_unit_param, decorate_with_various_unit, asqarray

from .calculus import *

from .plot import setup_matplotlib

from .units import m, s, kg, A, cd, K, mol, rad, sr
from .units import SI_units, SI_units_prefixed, SI_derived_units, other_units, units, all_units, SI_derived_units_prefixed
