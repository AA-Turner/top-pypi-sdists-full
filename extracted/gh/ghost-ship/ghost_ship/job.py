from jinja2 import Environment, PackageLoader, FileSystemLoader
import nomad, os, exception, loader, time, tyk
from urlparse import urlparse
import logging

FORMAT = '[GHOST SHIP] - [%(levelname)s]\t - %(message)s'

loglevel = os.environ.get('GHOSTSHIP_LOGLEVEL', 'info')
level = getattr(logging, loglevel.upper(), None)
logging.basicConfig(format=FORMAT, level=level)

NOMAD_ADDR = os.environ['NOMAD_ADDR']
nomad_url_object = urlparse(NOMAD_ADDR) 

nomad_client = nomad.Nomad(nomad_url_object.hostname,timeout=5)
# base_env for jobs and groups templates
base_env = Environment(loader=PackageLoader('ghost_ship', 'templates'))
# context env for jobs
logging.info('Current directory: %s' % os.getcwd())

cont_env = Environment(loader=FileSystemLoader(os.getcwd() + '/templates'))

class Job:
  def __init__(self, name):
    self.name = name
    self.groups = {
      'green': self.default_for('green'),
      'blue': self.default_for('blue')
    }

  def default_for(self, group_name):
    return {
      'service_name': self.name,
      'version': 'latest',
      'count': 0,
      'group': group_name
    }

  def run(self):
    print loader.run(loader.write(self.name, self.render()))

  def initilize(self, version):
    self.groups['green']['version'] = version
    del self.groups['green']['count']
    self.run()
    logging.info('Initilized with version %s' % version)
    try:
      tyk.reload(self.name, 'green')
    except exception.TykServiceNotFound:
      logging.info('Missing tyk service, tyk need manual config')


  def upgrade(self, version='0'):
    self.inspect()
    next = 'green' if self.current == 'blue' else 'blue'

    logging.info('Current state: %s' % self.current)
    logging.info('Next state: %s' % next)

    logging.info('Current version: %s' % self.groups[self.current]['version'])
    logging.info('Do upgrade to: %s' % version)

    self.groups[next]['count'] = self.groups[self.current]['count']
    self.groups[next]['version'] = version
    
    logging.debug(self.groups)
    self.run()
    if self.waiting(next):
      tyk.reload(self.name, next) 
      logging.info('Adjust count of %s to 0' % self.current)
      self.groups[self.current]['count'] = 0
      self.run()
    else:
      logging.error('Upgrade failed, rollback to %s' % self.current)
      self.groups[next]['count'] = 0
      self.run()
      exit(1)

  def scale(self, count=1):
    self.inspect() 
    logging.info('Scale %s to %s' % (self.current, count))
    self.groups[self.current]['count'] = count
    self.run()
    self.waiting(self.current)
    logging.info('What is done is done')

  def rollback(self):
    pass

  def inspect(self):
    try:
      job_info = nomad_client.job[self.name]
    except:
      raise exception.JobNotFound(self.name)

    for group in job_info['TaskGroups']:
      group_name = group['Name']
      instances_count = group['Count']

      image_version = (group['Tasks'][0]['Config']['image']).split(':')[1]

      self.groups[group_name] = {
        'service_name': self.name,
        'count': instances_count,
        'version': image_version,
        'group': group_name
      }

    self.current = 'green' if self.groups['green']['count'] >= self.groups['blue']['count'] else 'blue'

  def render_context(self, name):
    try:
      return cont_env.get_template(self.name + '.nomad.jinja').render(**self.groups.get(name, self.default_for('name')))
    except:
      raise exception.JobTemplateIsNotFound(self.name)

  def render_group(self, name):
    return base_env.get_template('group.nomad.jinja').render(group_name=name, content=self.render_context(name))

  def render(self):
    data = {
      'green': self.render_group('green'),
      'blue': self.render_group('blue'),
      'job_name': self.name
    }
    return base_env.get_template('job.nomad.jinja').render(**data)

  def waiting(self, group_name):
    running = True
    logging.info('Starting containers...', dict(continued=True))
    while (running):
      logging.info('...')
      j = nomad_client.jobs[self.name]
      logging.debug(j['JobSummary']['Summary'][group_name])
      running = j['JobSummary']['Summary'][group_name]['Starting'] != 0
      time.sleep(5)

    return j['JobSummary']['Summary'][group_name]['Running'] == self.groups[group_name]['count']
