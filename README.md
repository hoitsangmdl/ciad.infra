CIAD.INFRA
----------

This is a concept reference implementation for automating CICD toolchain setup, and cookie-cutting a working sample application with build/release/deploy tasks. It's written in ansible, python, and vagrant.

The CICD toolchain includes:
    1. OracleXE, Artifactory
    2. JIRA, BitBucket, and Jenkins.
    3. ELK and Nagios for reporting and monitoring.

The project template includes:
    1. A 'HelloWorld' simple java web application
    2. Deployment task (including provisioning a Tomcat VM)
    3. Jenkins JobDSL sample to generate build,release,deployment jobs

Please also be aware that:
    1. Default login for all system: admin/password
    2. Ensure the Project Template is "public readable" (under 'Register Project Templates') step


1. Setup
-----
**1. Prerequisites software**

To run this RI, please ensure you have 10gb ram and 20gb disk space. The following softwares are required:

    1. [Oracle VirtualBox](https://www.virtualbox.org/wiki/Downloads)
    2. [Vagrant](https://www.vagrantup.com/downloads.html)
    3. Python 2.7.x - You should have this by default in the OS (linux or mac).
    4. [OracleXE database](http://technet.oracle.com), and place the RPM file (e.g. oracle-xe-11.2.0-1.0.x86_64.rpm) into ./roles/oraclexe/files/oracle-xe-11.2.0-1.0.x86_64.rpm

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

2. Start up
-----------
All commands will be running within the same session after activating virtualenv.

    source env/bin/activate && vagrant up oracle elk jenkins elk

3. Register Project Templates
--------------------------
**1. Setup Inventory**

    source env/bin/activate && make template_setup

After this step, visit http://bitbucket:7990/projects/PROJTMPL/, and Ensure the Project Template is "public readable" in project repo settings

4. Create Sample Project
-----------------------
**1. export the following environment variables and run command**

    export PROJECT_KEY="HOIA"
    export PROJECT_SLUG="Project A for Hoi"
    make project_setup

After this step, visit generated artifacts:

    1. Bitbucket: http://bitbucket:7990/projects/HOIA
    2. Jira: http://jira:8080/HOIA/
    3. Jenkins: http://jenkins:8080/job/HOIA-helloworld-snapshot-build/

**2. Run Sample project build job**

In Jenkins, manually build the project:

    http://jenkins:8080/job/HOIA-helloworld-snapshot-build/

**3. Startup Dev runtime (Tomcat)**

    git clone http://bitbucket:7990/projects/HOIA/repos/helloworld-deploy/
    cd [helloworld-deploy] && vagrant up

Visit: http://tomcat:8080/HelloWorld, you should see 404 page not found.

**4. Run Sample Project deploy job**

    Jenkins: http://jenkins:8080/job/HOIA-helloworld-snapshot-deploy/

After the deployment is completed, visit http://tomcat:8080/HelloWorld, you should see Helloworld page.
