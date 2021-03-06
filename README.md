# Dynamic Inventory Use Case

#### Goal: Target instances in Shared Subtenant from a subtenant (Subtenant-Test-01) and execute an ansible task.

#### Example: Execute ansible task from Subtenant Test01 which targets Instance aa-ssr-testdns-01 in Shared Subtenant

#### User Story:
Master tenant has all the cloud added and assigned to subtenants. Cloud A added in master tenant is assigned to Shared subtenant and Subenant-Test-01. Ansible and git integrations are added to Master tenant. Tasks and workflows are created in Master tenant and workflows are made public for comsumption by subtenants. A Catalog item of type Operational workflow is created in Master tenant which consists of a few tasks. Below diagram shows the tasks in the workflow and what they would do.

![Workflow](/src/airbus_anisble.png?raw=true "Workflow")
<!-- <img src="/src/airbus_ansible.png" alt="workflow" width="80%"/> -->

Subtenants like "Subtenant-test-01" will have catalogs to request VM's with Operating systems like Centos, Windows etc. These VM's would use some shared services which are provided by VM's in Shared Subtenant like DNS etc. There is a provisioning workflow attached to the instance type layout which is for VM's like Centos, Windows etc. The workflow has some ansible tasks which are executed during the post provisioning phase of the VM. The Operational workflow will request this catalog from its task and then the next task would be to run ansible playbook in local context to target certain VM's using dynamic inventory plugin in the same subtenant. Once that is completed it will executed the next ansible task will target the VM's in the Shared subtenant.


Steps to achieve this use case.

- Install dynamic inventory plugin on all app servers. Refer doc [here](https://github.com/gomorpheus/ansible-collection-morpheus-core#readme)
- The morpheusinv.yml file can be multiple in different directories. Eg. below is the structure I used
```
        ├── /var/opt/morpheus/morpheus-ui/dynamic_inv
        │   ├── MT
        │   │   ├── morpheusinv.yml
        │   ├── SSR
        │   │   ├── morpheusinv.yml
        │   ├── ST
        └── └── └── morpheusinv.yml
```

- Catalog Items
![Catalog Items](/src/catalogItems.png?raw=true "Catalog Items")

The first one Onbaording has an operation workflow "orderCatalogUbuntu"

<img src="/src/ocUbuntu.png" alt="Catalog Ubuntu VM" width="50%"/>

The first python task in the workflow is associated to the script "**ubuntu-ct.py**" This script would trigger an API to order catalog Item "*Ubuntu 20.04*". The ubuntu 20.04 catalog items is of type instance which would provision an Ubuntu VM in the cloud which the subtenant has access. 

Once the instance is provisioned, the next ansible task in the workflow "*Base - local*" would execute. 

![Ansible task for Subtenant-Test-01](/src/baseLocal.png?raw=true "Base Local")

The execute target would be *local* and the command options would be using the dynamic inventory for ST01 in */var/opt/morpheus/morpheus-ui/dynamic_inv/ST01/morpheusinv.yml*

![ST inventory file](/src/STinv.png?raw=true "Invenory file")

This would generate 2 ansible groups **ubuntu-st01** **ubuntu-st02**. All instances with label ubuntu would be assigned to ubuntu-st01 and instances with label ubuntu-st02 will be assigned to ubuntu-st02. The playbook base.yml will be executed on all hosts for these 2 groups.

**Important**: Instances would be fetched from the tenant of which the user api key belongs to.

Once completed and successful it will trigger the next task **executeUpdateDNS**

<img src="/src/updateDNS.png" alt="Update DNS task" width="50%"/>

This python task would do an api call to search a workflow with name *execute+update+dns*. The workflow will execute a python task **updateDNS.py**. this script would order a catalog item visible in private shared subtenant called Update DNS. The script will use cypher to fetch the accessToken a private shared subtenant user. The token should be available in the Subtenant-Test-01. The access of the cypher can be controlled via a cypher policy in the subtenant.

<img src="/src/ocUpdateDNS.png" alt="Catalog Update DNS" width="50%"/>

The workflow associated to this catalog item has an ansible task which would execute and create DNS records etc.

<img src="/src/ssrUpdateDNS.png" alt="Catalog Ubuntu VM" width="50%"/>

The ansible task will target the inventory file */var/opt/morpheus/morpheus-ui/dynamic_inv/SSR/morpheusinv.yml*

The yaml file will generate an inventroy by searching all instance with label dns and executing the playbook against that instance.