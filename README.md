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

# Horizon Development Tool

```sh
./run_tests.sh --runserver 0.0.0.0:8877
```

* Creating default dashboard and panel directory structure
```sh
# Dashboard
mkdir openstack_dashboard/dashboards/mydashboard
./run_tests.sh -m startdash mydashboard --target openstack_dashboard/dashboards/mydashboard

# Panel inside `mydashboard`
mkdir openstack_dashboard/dashboards/mydashboard/mypanel
./run_tests.sh -m startpanel mypanel --dashboard=openstack_dashboard.dashboards.mydashboard --target=openstack_dashboard/dashboards/mydashboard/mypanel
```

* Horizon Start Scripts
```sh
nano /opt/stack/horizon/openstack_dashboard/enabled/_50_integra.py

# File:
DASHBOARD = 'integra'
DISABLED = False
ADD_INSTALLED_APPS = [ 'openstack_dashboard.dashboards.integra', ]
```

# Storage: Cinder

# Pandas Chart at Admin admin/overview
See: 
* [openstack_dashboard/dashboards/admin/overview/views.py](openstack_dashboard/dashboards/admin/overview/views.py)
* [openstack_dashboard/dashboards/admin/overview/templates/overview/usage.html](openstack_dashboard/dashboards/admin/overview/templates/overview/usage.html)
