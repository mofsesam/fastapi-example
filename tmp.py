import yaml, json
from collections import OrderedDict

data_dict = OrderedDict(json.load(open("tmp.json")))

with open("tmp2.yaml",'w') as f:
    f.write(yaml.dump(data_dict))