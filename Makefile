pyaddon:
	easy_install pip==1.2 && pip install virtualenv

setup:
	virtualenv env && . env/bin/activate && pip install ansible==2.0.0.2 requests bitbucket-api jenkinsapi
	git clone https://github.com/pycontribs/jira.git
	. env/bin/activate && cd jira && python setup.py install

restartvb:
	sudo /Library/Application\ Support/VirtualBox/LaunchDaemons/VirtualBoxStartup.sh restart

local_repo:
	export ANSIBLE_HOST_KEY_CHECKING=false && \
	ansible-playbook compact.yml \
	-i ./.vagrant/provisioners/ansible/inventory/vagrant_ansible_inventory --tags local_repo

monitored:
	export ANSIBLE_HOST_KEY_CHECKING=false && \
	ansible-playbook compact.yml \
        -i ./.vagrant/provisioners/ansible/inventory/vagrant_ansible_inventory --tags monitored

template_setup:
	echo "[local]\nlocalhost ansible_connection=local" >> ./.vagrant/provisioners/ansible/inventory/vagrant_ansible_inventory
	export ANSIBLE_HOST_KEY_CHECKING=false && \
	ansible-playbook -c local template.yml \
	-i ./.vagrant/provisioners/ansible/inventory/vagrant_ansible_inventory 

project_setup:
	export ANSIBLE_HOST_KEY_CHECKING=false && \
	ansible-playbook -c local project.yml \
	-i ./.vagrant/provisioners/ansible/inventory/vagrant_ansible_inventory \
	-e "project_key='$(PROJECT_KEY)' project_name='$(PROJECT_SLUG)'" 

up:
	. env/bin/activate && vagrant up oracle elk jenkins jira

destroy:
	. env/bin/activate && vagrant destroy oracle elk jenkins jira -f
