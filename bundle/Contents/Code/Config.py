# system
import os
import yaml

config_file_path = os.path.dirname(__file__) + '/../config.yml'

try:
  env = open(os.path.dirname(__file__) + '/../env', 'r').read()
except IOError:
  env = 'release'

C = yaml.load(open(config_file_path, 'r').read())[env]