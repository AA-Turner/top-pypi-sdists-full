# -*- coding: utf-8 -*-
"""
@author: Noemi E. Cazzaniga - 2024
@email: noemi.cazzaniga@polimi.it
"""


## Examples in README.md


import eurostat

toc = eurostat.get_toc()
print('get_toc =')
for el in range(0,5):
	print(toc[el])

toc_df = eurostat.get_toc_df()
print('get_toc_df =')
print(toc_df)

df = eurostat.subset_toc_df(toc_df, 'fleet')
print('subset_toc_df =')
print(df)

pars = eurostat.get_pars('demo_r_d2jan')
print('pars =')
print(pars)

par_values = eurostat.get_par_values('demo_r_d2jan', 'sex')
print('par_values =')
print(par_values)

dic = eurostat.get_dic('demo_r_d2jan')
print('dic =')
print(dic)

dic = eurostat.get_dic('demo_r_d2jan', 'sex', frmt='df')
print('dic =')
print(dic)

data = eurostat.get_data('GOV_10DD_SLGD')
print('data[0] =')
print(data[0])
print('data[90:95] =')
print(data[90:95])

data = eurostat.get_data('GOV_10DD_SLGD', True)
print('data[0] =')
print(data[0])
print('data[90:95] =')
print(data[90:95])

code = 'GOV_10DD_SLGD'
pars = eurostat.get_pars(code)
print('pars =')
print(pars)
par_values = eurostat.get_par_values(code, 'geo')
print('par_values= ')
print(par_values)
my_filter_pars = {'startPeriod': 2019, 'geo': ['AT','BE']}
data = eurostat.get_data(code, filter_pars=my_filter_pars)
print('data[0] =')
print(data[0])
print('data[445:447] =')
print(data[445:447])

code = 'GOV_10DD_SLGD'
pars = eurostat.get_pars(code)
print('pars =')
print(pars)
par_values = eurostat.get_par_values(code, 'geo')
print('par_values= ')
print(par_values)
my_filter_pars = {'startPeriod': 2019, 'geo': ['AT','BE']}
data = eurostat.get_data(code, True, filter_pars=my_filter_pars)
print('data[0] =')
print(data[0])
print('data[446:448] =')
print(data[446:448])

data = eurostat.get_data_df('GOV_10DD_SLGD')
print('data =')
print(data)

data = eurostat.get_data_df('GOV_10DD_SLGD', True)
print('data =')
print(data)

code = 'GOV_10DD_SLGD'
pars = eurostat.get_pars(code)
print('pars =')
print(pars)
par_values = eurostat.get_par_values(code, 'geo')
print('par_values= ')
print(par_values)
my_filter_pars = {'endPeriod': 2020, 'geo': ['AT','BE']}
data = eurostat.get_data_df(code, filter_pars=my_filter_pars)
print('data =')
print(data)

code = 'GOV_10DD_SLGD'
pars = eurostat.get_pars(code)
print('pars =')
print(pars)
par_values = eurostat.get_par_values(code, 'geo')
print('par_values= ')
print(par_values)
my_filter_pars = {'endPeriod': 2020, 'geo': ['AT','BE']}
data = eurostat.get_data_df(code, True, filter_pars=my_filter_pars)
print('data =')
print(data)
