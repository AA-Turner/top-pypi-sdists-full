import math
import numpy as np
import itertools
import pandas as pd
from decimal import Decimal
from fractions import Fraction
from colored import Fore, Back, Style
from radboy.DB.db import std_colorize

def dsp(ftext):
	msg=[f"{Fore.orange_red_1}{ftext}{Style.reset}",
	f"{Fore.light_cyan}= {Fore.light_green}{eval(ftext)}{Style.reset}"]
	cta=len(msg)
	for num,i in enumerate(msg):
		print(std_colorize(i,num,cta))