import requests

r = requests.get('https://www.meethue.com/api/nupnp')
x = r.json()
for item in x:
    print dict(item)['internalipaddress']
