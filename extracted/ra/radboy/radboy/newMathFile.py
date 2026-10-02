from pathlib import Path
from datetime import datetime
import tarfile
home=Path(".")
package=home/Path("math_files.tar.gz")
Dir=f"{home}/Math.d/"
Dir=Path(Dir)
if not Dir.exists():
    Dir.mkdir(parents=True)


file=Dir/Path(f"mathFile-{datetime.now().strftime('%m_%d_%Y-%H_%M_%S')}.py")

script="""import numpy as np 
import pandas as pd 
import sympy as sp 
import os,sys 
import random 
def randomFloat():
    n=random.random()
    multiplier=random.randint(0,100)
    resolution=random.randint(0,3)

    r=float(f'{(n*multiplier):.{resolution}f}')
    return r

c_fmla=sp.symbols('c_fmla')
equals_fmla=randomFloat()

rf1=randomFloat()
rf2=randomFloat()

exp_fmla=f'({rf1}*({rf2}+c_fmla))={equals_fmla}'
expression_fmla_hide=sp.Eq(rf1*(rf2+c_fmla),equals_fmla)

solution_fmla_hide=sp.solve(expression_fmla_hide)
"""
with file.open("w") as out:
    out.write(script)
print("ScriptFile: ",file)

with tarfile.open(package,"w:gz") as gzf: 
    gzf.add(Dir)
print("DataFiles: ",package)
