project('mi_proyecto_joaquin_vft', 'c', 'fortran', version: '0.1.12')

# 1. Capturar los valores de las opciones (desde pip o por defecto)
ns_arg = get_option('NS').to_string()
nv_arg = get_option('NV').to_string()

# 2. Definir los argumentos del compilador
# -cpp: Fuerza el preprocesador en gfortran para archivos .f90
fortran_args = [
    '-cpp',
    '-frecursive',
    '-fstack-arrays',
    '-DNS_VAL=' + ns_arg,
    '-DNV_VAL=' + nv_arg
]

# Argumentos para C (f2py genera código C que usa estas macros)
# Añadimos versiones en minúsculas porque el error indica que busca 'ns' y 'nv'
c_args_especificos = [
    '-DVOFTOOLS_NS=' + ns_arg, 
    '-DVOFTOOLS_NV=' + nv_arg
]

# Aplicar los argumentos a todo el proyecto
add_project_arguments(fortran_args, language: 'fortran')
#add_project_arguments(c_args, language: 'c')

# 3. Importar el módulo de Python
py = import('python').find_installation(pure: false)

# 4. Obtener directorios de inclusión para NumPy y F2PY
# Esto es necesario para que f2py encuentre las cabeceras de enlace
# Rutas de cabeceras (headers)
incdir_numpy = run_command(py, ['-c', 'import numpy; print(numpy.get_include())'], check: true).stdout().strip()
incdir_f2py = run_command(py, ['-c', 'import numpy.f2py; import os; print(os.path.join(os.path.dirname(numpy.f2py.__file__), "src"))'], check: true).stdout().strip()

# Definir el directorio donde está dimpol.h
inc_src = include_directories('src')

# 5. Definir la extensión de Python (el wrapper de Fortran)
py.extension_module(
    'mi_proyecto_joaquin_vft',
    sources: [
        'src/voftools.f90',               # Tu código original
        'src/voftools-f2pywrappers2.f90', # El wrapper F90 generado
        'src/voftoolsmodule.c',           # El wrapper C generado
        'src/fortranobject.c'             # El objeto base de f2py que copiamos
    ],
    include_directories: [inc_src, incdir_numpy, incdir_f2py],
    fortran_args: fortran_args,           # Pasar las macros NS_VAL y NV_VAL a f2py
    c_args: c_args_especificos,
    install: true
)

