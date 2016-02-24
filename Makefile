pyaddon:
	easy_install pip==1.2 && pip install virtualenv

setup:
	virtualenv env && . env/bin/activate && pip install ansible==2.0.0.2 requests bitbucket-api jenkinsapi
	rm -rf jira
	git clone https://github.com/pycontribs/jira.git
	. env/bin/activate && cd jira && python setup.py install

restartvb:
	sudo /Library/Application\ Support/VirtualBox/LaunchDaemons/VirtualBoxStartup.sh restart

local_repo:
	. env/bin/activate && \
	export ANSIBLE_HOST_KEY_CHECKING=false && \
	ansible-playbook compact.yml \
	-i ./.vagrant/provisioners/ansible/inventory/vagrant_ansible_inventory --tags local_repo

monitored:
	. env/bin/activate && \
	export ANSIBLE_HOST_KEY_CHECKING=false && \
	ansible-playbook compact.yml \
        -i ./.vagrant/provisioners/ansible/inventory/vagrant_ansible_inventory --tags monitored

template_setup:
	. env/bin/activate && \
	echo "[local]\nlocalhost ansible_connection=local" >> ./.vagrant/provisioners/ansible/inventory/vagrant_ansible_inventory && \
	export ANSIBLE_HOST_KEY_CHECKING=false && \
	ansible-playbook -c local template.yml \
	-i ./.vagrant/provisioners/ansible/inventory/vagrant_ansible_inventory 

project_setup:
	. env/bin/activate && \
	export ANSIBLE_HOST_KEY_CHECKING=false && \
	ansible-playbook -c local project.yml \
	-i ./.vagrant/provisioners/ansible/inventory/vagrant_ansible_inventory \
	-e "project_key='$(PROJECT_KEY)' project_name='$(PROJECT_SLUG)'" 

up:
	. env/bin/activate && vagrant up oracle elk jenkins jira

destroy:
	vagrant destroy oracle elk jenkins jira -f

reload:
	rm -rf env jira && make destroy
	time sh -c 'export PROJECT_KEY="HOIA" && export PROJECT_SLUG="Project A for Hoi" && sudo make pyaddon && make setup up && sleep 90 && make template_setup project_setup'
