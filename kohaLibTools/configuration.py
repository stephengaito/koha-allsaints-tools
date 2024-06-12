
import os
import yaml

# we look for the `config.yaml` configuration in the following three places:

etcPath = os.path.join('/etc', 'kohaTools', 'config.yaml')

userPath = os.path.join(
  os.path.expanduser('~'),
  '.config', 'kohaTools', 'config.yaml'
)

localPath = os.path.join('config.yaml')

config = {}

try :
  with open(etcPath) as etcFile :
    config = yaml.safe_load(etcFile.read())
except :
  try :
    with open(userPath) as userFile :
      config = yaml.safe_load(userFile.read())
  except :
    try :
      with open(localPath) as localFile :
        config = yaml.safe_load(localFile.read())
    except :
      print("Could not load external configuration")

dbConfig = {}
if 'database' in config : dbConfig = config['database']

kohaConfig = {}
if 'koha' in config : kohaConfig = config['koha']
if 'baseUrl' not in kohaConfig : kohaConfig['baseUrl'] = ''
if 'overdueDays' not in kohaConfig : kohaConfig['overdueDays'] = 7
