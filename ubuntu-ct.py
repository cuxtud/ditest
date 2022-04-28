import requests, time, sys, json

# Morpheus Globals
MORPHEUS_VERIFY_SSL_CERT = False
MORPHEUS_HOST = morpheus['morpheus']['applianceHost']
MORPHEUS_TENANT_TOKEN = morpheus['morpheus']['apiAccessToken']
MORPHEUS_HEADERS = {"Content-Type":"application/json","Accept":"application/json","Authorization": "Bearer " + MORPHEUS_TENANT_TOKEN} 

def orderCatalog(gid):
    jbody = {"order": {"items": [{"type": {"name": "Ubuntu 20.04"},"config": {"groups": gid,"clouds": 1}}]}}
    body = json.dumps(jbody)
    url = 'https://%s/api/catalog/orders' % (MORPHEUS_HOST)
    response = requests.post(url, headers=MORPHEUS_HEADERS, body=body, verify=MORPHEUS_VERIFY_SSL_CERT)
    data = response.json()

def getGroupId():
    url = 'https://%s/api/groups?phrase=all' % (MORPHEUS_HOST)
    response = requests.get(url, headers=MORPHEUS_HEADERS), verify=MORPHEUS_VERIFY_SSL_CERT
    data = response.json()
    gid = data['groups'][0]['id']
    return gid

def main():
    gid=getGroupId()
    orderCatalog(gid)
 
if __name__ == "__main__":
    main()