pyaddon:
	easy_install pip==1.2 && pip install virtualenv

setup:
	virtualenv env && . env/bin/activate && pip install ansible==1.9.4 requests bitbucket-api jenkinsapi
	git clone https://github.com/pycontribs/jira.git
	. env/bin/activate && cd jira && python setup.py install

restartvb:
	sudo /Library/Application\ Support/VirtualBox/LaunchDaemons/VirtualBoxStartup.sh restart


setup_inventory:
	cat /etc/ansible/hosts >> ./.vagrant/provisioners/ansible/inventory/vagrant_ansible_inventory

template_setup:
	ansible-playbook -c local template_setup.yml \
	-i ./.vagrant/provisioners/ansible/inventory/vagrant_ansible_inventory 

project_setup:
	ansible-playbook -c local project.yml \
	-i ./.vagrant/provisioners/ansible/inventory/vagrant_ansible_inventory \
	-e "project_key='$(PROJECT_KEY)' project_name='$(PROJECT_SLUG)'" 

test_jenkins:
	ansible jenkins -i ./.vagrant/provisioners/ansible/inventory/vagrant_ansible_inventory -a "ls -l" -vvvv
