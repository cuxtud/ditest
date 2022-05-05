# Dynamic Inventory Use Case

#### Goal: Target instances in Shared Subtenant from a subtenant (Subtenant-Test-01) and execute an ansible task.

#### Example: Execute ansible task from Subtenant Test01 which targets Instance aa-ssr-testdns-01 in Shared Subtenant

#### User Story:
Master tenant has all the cloud added and assigned to subtenants. Cloud A added in master tenant is assigned to Shared subtenant and Subenant-Test-01. Ansible and git integrations are added to Master tenant. Tasks and workflows are created in Master tenant and workflows are made public for comsumption by subtenants. A Catalog item of type Operational workflow is created in Master tenant which consists of a few tasks. Below diagram shows the tasks in the workflow and what they would do.

![Workflow](/src/DI01.png?raw=true "Workflow")

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
        │   ├── SSR
        └── └── └── morpheusinv.yml
```

- Catalog Items
![Catalog Items](/src/catalogItems.png?raw=true "Catalog Items")