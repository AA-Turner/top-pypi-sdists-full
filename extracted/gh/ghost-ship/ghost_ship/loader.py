import subprocess

def write(name, content):
  filename = '/tmp/' + name + '.nomad'
  f = open(filename, 'w')
  f.write(content)
  f.close()
  return filename

def run(filename):
  return subprocess.check_output(['nomad', 'run', filename])  
