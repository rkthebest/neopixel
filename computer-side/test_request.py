import requests
import sys

data = {"state":"{}".format(sys.argv[2])}
resp = requests.post('http://10.12.19.195:5555/led/{}/'.format(sys.argv[1]), json=data)