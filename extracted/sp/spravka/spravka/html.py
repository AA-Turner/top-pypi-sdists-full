import os

def html():
    os.chdir('docs')
    os.system('make html')
    os.chdir('..')