/*##################################################################################################
# This file is a part of PyPartMC licensed under the GNU General Public License v3 (LICENSE file)  #
# Copyright (C) 2022 University of Illinois Urbana-Champaign                                       #
# Authors: https://github.com/open-atmos/PyPartMC/graphs/contributors                              #
##################################################################################################*/

#pragma once

extern "C" void py_pow2_above(int*, int*);
extern "C" void f_sphere_vol2rad(const double*, double*);
extern "C" void f_rad2diam(const double*, double*);
extern "C" void f_sphere_rad2vol(const double*, double*);
extern "C" void f_diam2rad(const double*, double*);

int pow2_above(int n);
double sphere_vol2rad(double v);
double rad2diam(double rad);
double sphere_rad2vol(double rad);
double diam2rad(double d);

extern "C" double py_deg2rad(double);

