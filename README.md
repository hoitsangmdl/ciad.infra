Overview
----------

This is a concept reference implementation for automating CICD toolchain setup, and cookie-cutting a working sample application plus related CICD tasks. It's written with ansible, python, and vagrant.

The CICD toolchain includes:
1. JIRA, BitBucket, Artifactory, and Jenkins.
2. OracleXE database and Proxy (squid) server.
3. Elasticsearch, Logstash, Collectd, and Nagios for reporting and monitoring.
4. Tomcat - just a sample web container to run helloworld from sample code

The database serve as backend for JIRA, BitBucket, and Artifactory. The Proxy server mimic a corporate environment (not enable by default). Sample project templates also included.

There are also 2 Vagrantfile:

1. Vagrantfile.master - 7 VMs (oracle, artifactory, jira, bitbucket, elk, nagios, jenkins)
2. Vagrantfile.compact - 4 VMs (oracle + artifactory, jira + bitbucket, elk + nagios, jenkins)

Use a symlink to shortcut into the proper Vagrantfile as selection.

**Default login for all system: admin/password**
**Ensure the Project Template is "public readable" (under 'Register Project Templates') step**

1. Setup
-----
**1. Required runtimes**

To run this RI, please ensure you have 16gb ram and 100gb disk space. The following softwares are required:

- [Oracle VirtualBox](https://www.virtualbox.org/wiki/Downloads)
- [Vagrant](https://www.vagrantup.com/downloads.html)
- Python 2.7.x - You should have this by default in the OS (linux or mac).

**2. Vagrant Image**

Please also ensure you have CentOS7 vagrant box installed. This RI is built with [this](http://cloud.centos.org/centos/7/vagrant/x86_64/images/CentOS-7-Vagrant-1509-x86_64-01.box) image. Other CentOS7 base image should work.

    vagrant add centos7.0 {image url}

**3. OracleXE rpm**

You will need to download [OracleXE database](http://technet.oracle.com), and place the RPM file (e.g. oracle-xe-11.2.0-1.0.x86_64.rpm) into ./roles/oraclexe/files/oracle-xe-11.2.0-1.0.x86_64.rpm

**4. Pip and virtualenv**

Please ensure you have **pip** and **virtualenv** installed. If unsure, please run the following to install pip and virtualenv:

    make pyaddon

To start after checkout the application, run the following to setup **virtualenv** and install required python dependencies:

    make setup

**5. /etc/hosts**

Some of the playbook require API interaction from local machine to the VM. The following DNS alias entries are required:

For vagrantfile.master, please add the following entries into /etc/hosts

    192.168.100.11   proxy
    192.168.100.12   oracle
    192.168.100.13   artifactory
    192.168.100.14   bitbucket
    192.168.100.15   jira
    192.168.100.16   jenkins
    192.168.100.17   elk
    192.168.100.18   nagios
    192.168.100.50	 tomcat

For Vagrantfile.compact, please add the following entries into /etc/hosts:

    192.168.100.11   proxy
    192.168.100.12   oracle
    192.168.100.12   artifactory
    192.168.100.15   bitbucket
    192.168.100.15   jira
    192.168.100.16   jenkins
    192.168.100.17   elk
    192.168.100.17   nagios
    192.168.100.50	 tomcats

2. Start up
-----------
**1. Activate python virtualenv**

This step will inject current the python runtime located at "{project folder}/env/bin/python" into \${PATH} variable ahead of default python runtime. All the python dependencies for projects (under **make setup** step) are installed in {project folder}/env/lib/python/site-packages".

    source ./env/bin/activate

**2. Startup orders (for Vagrantfile.master):**

The VMs in the toolchain have dependencies. They need to be started in the following orders:

    # 1. install oracle and artifactory
    vagrant up oracle artifactory

    # 2. register license into artifactory manually
    # visit http://artifactory:8081

    # 3. repoint both oracle and artifactory to use artifactory as yum repo
    vagrant provision oracle artifactory

    # 4. setup nagios and elk
    vagrant up nagios elk

    # 5. repoint systems to nagios and elk for monitoring
    vagrant provision oracle artifactory nagios elk

    # visit http://nagios/nagios
    # visit http://elk:5602/

    # 6. setup jira bitbucket jenkins
    vagrant up jira bitbucket jenkins

    # 7. manually register jira and bitbucket
    # visit http://jira:8080
    # visit http://bitbucket:7990

**3. Startup orders (for Vagrantfile.compact):**

The VMs in the toolchain have dependencies. They need to be started in the following orders:

    # 1. install oracle + artifactory
    vagrant up oracle

    # 2. register license into artifactory manually
    # visit http://artifactory:8081

    # 3. repoint both oracle and artifactory to use artifactory as yum repo
    vagrant provision oracle

    # 4. setup nagios and elk
    vagrant up elk

    # 5. repoint systems to nagios and elk for monitoring
    vagrant provision oracle elk

    # visit http://nagios/nagios
    # visit http://elk:5602/

    # 6. setup jira bitbucket jenkins
    vagrant up jira jenkins

    # 7. manually register jira and bitbucket
    # visit http://jira:8080
    # visit http://bitbucket:7990


3. Register Project Templates
--------------------------
**1. Setup Inventory**
In vagrant generated inventory file (./.vagrant/provisioners/ansible/inventory/vagrant_ansible_inventory), ensure the [local] connection exists:

    [local]
    localhost ansible_connection=local

**2. Setup Template**
This step will upload sample templates (helloworld, helloworld-jobdsl, helloworld-deploy) into bitbucket

    make template_setup

After this step, visit http://bitbucket:7990/projects/PROJTMPL/

**3. Ensure the Project Template is "public readable" in project repo settings**
Or else the followings will fail.

4. Create Sample Project
-----------------------
**1. Setup Sample Projects**
In your shell environment, export the following environment variables:

    export PROJECT_KEY="HOIA"
    export PROJECT_SLUG="Project A for Hoi"

After that, in the same shell, run the following command:

    make project_setup

After this step, visit generated artifacts:

    1. Bitbucket: http://bitbucket:7990/projects/HOIA
    2. Jira: http://jira:8080/HOIA/
    3. Jenkins: http://jenkins:8080/job/HOIA-helloworld-snapshot-build/

**2. Run Sample project build job**

In Jenkins, manually build the project:

    http://jenkins:8080/job/HOIA-helloworld-snapshot-build/

**3. Startup Dev runtime (Tomcat)**

In local shell, check out bitbucket:7990/projects/HOIA/repos/helloworld-deploy/.
Go into the checked out directory, use the included Vagrantfile to startup tomcat.

    cd [helloworld-deploy] && vagrant up

Visit: http://tomcat:8080/HelloWorld, you should see 404 page not found.

**4. Run Sample Project deploy job**

    Jenkins: http://jenkins:8080/job/HOIA-helloworld-snapshot-deploy/

After the deployment is completed, visit http://tomcat:8080/HelloWorld, you should see Helloworld page.
