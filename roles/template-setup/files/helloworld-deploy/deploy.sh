#!/bin/bash
server=http://artifactory:8081/artifactory
repo={{project_key|lower}}
name={{repo_name}}
artifact=com/mckinsey/$name
path=$server/$repo/$artifact
version=`curl -s $path/maven-metadata.xml | grep latest | sed "s/.*<latest>\\([^<]*\\)<\\/latest>.*/\\1/"`
build=`curl -s $path/$version/maven-metadata.xml | grep '<value>' | head -1 | sed "s/.*<value>\\([^<]*\\)<\\/value>.*/\\1/"`
url=$path/$version/$name-$build.war

virtualenv env && . env/bin/activate && pip install ansible
export ANSIBLE_HOST_KEY_CHECKING=False
chmod 600 insecure_private_key
ansible-playbook deploy.yml \
  -i inventory --limit=dev \
  -e "war_repo_src_url=${url} \
      war_deployed_path=/var/lib/tomcat/webapps/$name.war \
      war_deployed_folder_path=/var/lib/tomcat/webapps/$name"
