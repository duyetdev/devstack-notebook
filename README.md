# devstack-notebook
Devstack (Openstack develope version) notebook by Raptors Team

# Config stack 
See [local.conf](local.conf)

# Fix Cinder when rejoin
```sh
sudo losetup /dev/loop0 /opt/stack/data/stack-volumes-default-backing-file
sudo losetup /dev/loop1 /opt/stack/data/stack-volumes-lvmdriver-1-backing-file

# rejoin
./rejoin-stack.sh
```
