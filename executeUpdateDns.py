import requests, sys , time, json

# Morpheus Globals
MORPHEUS_VERIFY_SSL_CERT = False
MORPHEUS_HOST = morpheus['morpheus']['applianceHost']
MORPHEUS_TENANT_TOKEN = morpheus['morpheus']['apiAccessToken']
MORPHEUS_HEADERS = {"Content-Type":"application/json","Accept":"application/json","Authorization": "Bearer " + MORPHEUS_TENANT_TOKEN} 

def getworkflowId():
    url = 'https://%s/api/task-sets?phrase=execute+update+dns' % (MORPHEUS_HOST)
    response = requests.get(url, headers = MORPHEUS_HEADERS, verify = MORPHEUS_VERIFY_SSL_CERT)
    if not response.ok:
        print("Error: Unable to get workflow with name Execute Update DNS : Response code %s: %s" % (response.status_code, response.text))
        raise Exception("Error: Unable to get workflow with name Execute Update DNS : Response code %s: %s" % (response.status_code, response.text))
    data = response.json()
    wid = data['taskSets'][0]['id']
    return wid

def executeWorkflow(wid):
    jbody = {"job": {}}
    print(json.dumps(jbody, indent=4))
    body = json.dumps(jbody)
    url = 'https://%s/api/catalog/orders' % (MORPHEUS_HOST)
    response = requests.post(url, headers = MORPHEUS_HEADERS, data = body, verify = MORPHEUS_VERIFY_SSL_CERT)
    if not response.ok:
        print("Error: Unable to execute workflow with id '%s' : Response code %s: %s" % (wid, response.status_code, response.text))
        raise Exception("Error: Unable to execute workflow with id '%s' : Response code %s: %s" % (wid, response.status_code, response.text))

def main():
    wid=getworkflowId()
    executeWorkflow(wid)
 
if __name__ == "__main__":
    main()