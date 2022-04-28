import requests, time, sys, json
from morpheuscypher import Cypher
c = Cypher(morpheus=morpheus,ssl_verify=False)
 
MORPHEUS_TENANT_TOKEN=str(c.get("secret/ssr"))

# Morpheus Globals
MORPHEUS_VERIFY_SSL_CERT = False
MORPHEUS_HOST = morpheus['morpheus']['applianceHost']
#MORPHEUS_TENANT_TOKEN = morpheus['morpheus']['apiAccessToken']
MORPHEUS_HEADERS = {"Content-Type":"application/json","Accept":"application/json","Authorization": "Bearer " + MORPHEUS_TENANT_TOKEN} 

def orderCatalog():
    jbody = {"order": {"items": [{"type": {"name": "Update DNS"},"context": "appliance"}]}}
    body = json.dumps(jbody)
    url = 'https://%s/api/catalog/orders' % (MORPHEUS_HOST)
    response = requests.post(url, headers = MORPHEUS_HEADERS, data = body, verify = MORPHEUS_VERIFY_SSL_CERT)
    data = response.json()
    print("")
    print("payload for catalog order post response")
    print("------------------------------------------")
    print(json.dumps(data, indent=4))

#MAIN
orderCatalog()