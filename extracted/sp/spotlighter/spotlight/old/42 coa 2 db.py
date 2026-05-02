# coa 2 db

import pandas as pd
import json
from mylib import myFileDialog as myfd

#File 2 
path = myfd.askopenfilename()
df = pd.read_excel(path)

