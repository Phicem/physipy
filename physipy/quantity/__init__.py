# !/usr/bin/env python
# -*- coding: utf-8 -*-

from .quantity import Dimension, Quantity
from .quantity import DimensionError, SI_UNIT_SYMBOL
from .quantity import quantify, make_quantity
from .utils import check_dimension, set_favunit, dimension_and_favunit, drop_dimension, decorate_with_various_unit

from .calculus import interp, linspace, vectorize, integrate_trapz, qroot, qbrentq
from .calculus import trapz, quad, dblquad, tplquad

from .units import m, s, kg, A, cd, K, mol, rad, sr
from .units import SI_units, SI_units_prefixed, SI_derived_units, other_units, units
