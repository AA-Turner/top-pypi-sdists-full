P=$(python -c "import os, pikobs; print(os.path.dirname(pikobs.__file__))" 2>/dev/null \
    || echo /fs/site8/eccc/cmd/cmda/dlo001/pikobs_install/env/lib/python3.10/site-packages/pikobs)

# 1. what each file actually defines
grep -n "^def arg_call\|^def make_scatter\|^FAMILY_CODES\|^def obscountdb_report" \
     $P/obscountdb/obscountdb.py $P/obscountdb/obscountdb_plot.py

# 2. sizes: obscountdb.py ronda las 700 líneas, obscountdb_plot.py unas 780
wc -l $P/obscountdb/*.py

# 3. import directo del fichero, sin el paquete
python -c "
import importlib.util as u, sys
spec = u.spec_from_file_location('m', '$P/obscountdb/obscountdb.py')
m = u.module_from_spec(spec); spec.loader.exec_module(m)
print([n for n in ('arg_call','make_scatter','FAMILY_CODES','TOTAL_VARNO') if hasattr(m, n)])"
