[main]
reposdir=/etc/reposync.repos.d

[local-vdsm-build-el7]
name=VDSM local built rpms
baseurl=file://@PWD@/exported-artifacts
enabled=1
gpgcheck=0

[ovirt-master-snapshot-el7]
name=oVirt Master Nightly Test Releases
baseurl=http://resources.ovirt.org/pub/ovirt-master-snapshot/rpm/el7/
exclude=vdsm-* ovirt-node-* *-debuginfo ovirt-engine-appliance ovirt*engine* *win* *jboss*
enabled=1
gpgcheck=0

[ovirt-master-snapshot-static-el7]
name=oVirt Master Nightly Statics
baseurl=http://resources.ovirt.org/pub/ovirt-master-snapshot-static/rpm/el7/
exclude=jasperreports-server ovirt-guest-tools-iso ovirt-engine-jboss-as *wildfly*
enabled=1
gpgcheck=0

[centos-ovirt40-candidate-el7]
name=CentOS-7 - oVirt 4.0
baseurl=http://cbs.centos.org/repos/virt7-ovirt-40-candidate/x86_64/os/
gpgcheck=0
enabled=1
