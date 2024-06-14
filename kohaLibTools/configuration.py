
import os
import sys
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

if 'password' not in dbConfig :
  print("CAN NOT connect to the Koha database without a password!!!")
  sys.exit(1)

# NOTE: if host is specified as `localhost` then the socket is used
# if host is specified as an IP address (`127.0.0.1`) the the port is used

if 'database' not in dbConfig : dbConfig['database'] = 'koha_allsaints'
if 'user'     not in dbConfig : dbConfig['user']     = 'koha_allsaints'
if 'host'     not in dbConfig : dbConfig['host']     = '127.0.0.1'
if 'port'     not in dbConfig : dbConfig['port']     = '3306'
if not isinstance(dbConfig['port'], int) :
  dbConfig['port'] = int(dbConfig['port'])

kohaConfig = {}
if 'koha' in config : kohaConfig = config['koha']
if 'baseUrl' not in kohaConfig : kohaConfig['baseUrl'] = ''
if 'overdueDays' not in kohaConfig : kohaConfig['overdueDays'] = 7
