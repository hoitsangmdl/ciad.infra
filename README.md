CIAD.INFRA
----------

__** YOU WILL NEED TO OBTAIN YOUR OWN SOFTWARE LICENSES! **__

This is a concept reference implementation for automating CICD toolchain setup, and cookie-cutting a working sample application with build/release/deploy tasks. It's written in ansible, python, and vagrant.

The CICD toolchain includes:

1. OracleXE
2. [Artifactory](http://artifactory:8081) 
3. [JIRA](http://jira:8080) (admin/password)
4. [BitBucket](bitbucket:7990) (admin/password)
5. [Jenkins](http://jenkins:8080) (admin/password)
6. [ELK](http://elk:5601)
7. [Nagios](http://nagios/nagios) (nagiosadmin/nagiosadmin)

The project template includes:

1. A 'HelloWorld' simple java web application
2. Deployment task (including provisioning a Tomcat VM)
3. Jenkins JobDSL sample to generate build,release,deployment jobs

To run this RI, please ensure you have 10gb ram and 20gb disk space.


1. Setup
-----
**1. Prerequisites software**

The following softwares are required:

1. [Oracle VirtualBox](https://www.virtualbox.org/wiki/Downloads)
2. [Vagrant](https://www.vagrantup.com/downloads.html)
3. Python 2.6.x - 2.7.x (included in Linux or OSX).
4. [OracleXE database](http://technet.oracle.com)

For OracleXE database, please place the RPM file from OracleXE database (e.g. oracle-xe-11.2.0-1.0.x86_64.rpm) into ./roles/oraclexe/files/oracle-xe-11.2.0-1.0.x86_64.rpm

**2. Pip, virtualenv, and python libraries**

Please ensure you have **pip** and **virtualenv** installed. If unsure, please run the following to install pip and virtualenv:

    sudo make pyaddon

To start after checkout the application, run the following to setup **virtualenv** and install required python dependencies:

    make setup

**3. /etc/hosts**

Last, some of the playbook require API interaction from local machine to the VM. The following DNS alias entries are required (e.g. add into /etc/hosts)

    192.168.100.11   proxy
    192.168.100.12   oracle
    192.168.100.13   artifactory
    192.168.100.14   bitbucket
    192.168.100.15   jira
    192.168.100.16   jenkins
    192.168.100.17   elk
    192.168.100.18   nagios
    192.168.100.50   tomcat

2. Start up Toolchain
-----------

    source env/bin/activate && vagrant up oracle elk jenkins jira

In the events of provisioning errors, please run the provisioning command:

    source env/bin/activate && vagrant provision elk jenkins jira

The script is wrritten as idempotent. Most of the errors encountered due to network connectivity.


3. Register Project Templates 
--------------------------

    source env/bin/activate && make template_setup

After this step, visit [Bitbucket Project Template](http://bitbucket:7990/projects/PROJTMPL/), and Ensure the Project Template is "public readable" in project repo settings

4. Create Sample Project
-----------------------
export the following environment variables and run command

    export PROJECT_KEY="HOIA"
    export PROJECT_SLUG="Project A for Hoi"
    make project_setup

5. Review, Build, and Deploy Sample Project
----------------------------
**1. Visit generated artifacts:**

1. [Bitbucket HOIA repo](Bitbucket: http://bitbucket:7990/projects/HOIA)
2. [Jira HOIA space](http://jira:8080/HOIA/)
3. [Jenkins HOIA view](http://jenkins:8080/view/HOIA)

**2. Startup Dev runtime (Tomcat)**

    git clone http://bitbucket:7990/projects/HOIA/repos/helloworld-deploy/
    cd [helloworld-deploy] && vagrant up

**3. Run Sample project build job and Deploy**

[Jenkins HOIA snapshot build](http://jenkins:8080/job/HOIA-helloworld-snapshot-build/)
[Jenkins HOIA snapshot deploy](http://jenkins:8080/job/HOIA-helloworld-snapshot-deploy/)

After the deployment is completed, visit http://tomcat:8080/HelloWorld, you should see Helloworld page.
