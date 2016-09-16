import requests
import re
import json


url='https://www.cavendishonline.co.uk/themes/Cavendish/js/fund_init.js'
r=requests.get(url)
s=r.text
r=re.match(r'var\s+fund_data\s*=\s*(\{.+\});\s*function\s+fund_init_setup',s,re.S)
st=r.groups()[0]
j = re.sub(r"{\s*'?(\w)", r'{"\1', st)
j = re.sub(r",\s*'?(\w)", r',"\1', j)
j = re.sub(r"(\w)'?\s*:", r'\1":', j)
j = re.sub(r":\s*'(\w+)'\s*([,}])", r':"\1"\2', j)
j[:100]
#j=json.loads(j)
#print(j['funds']['0145150']['name'])
