Vagrant.configure("2") do |config|

  config.vm.box = "bento/centos-7.1"
  config.vm.synced_folder ".", "/home/vagrant/sync", disabled: true
  config.ssh.insert_key = false
  config.vm.provider :virtualbox do |vb|
    vb.customize ["modifyvm", :id, "--cpus", "2"]
  end

  config.vm.define "oracle" do |v|
    v.vm.host_name = "oracle"
    v.vm.network "private_network", ip: "192.168.101.12"
    v.vm.network "private_network", ip: "192.168.101.13"
    config.vm.provider :virtualbox do |vb|
      vb.customize ["modifyvm", :id, "--memory", "4096"]
    end
    v.vm.provision "ansible" do |ansible|
      ansible.playbook = "compact.yml"
      ansible.limit = "oracle"
    end
  end

  config.vm.define "jira" do |v|
    v.vm.host_name = "jira"
    v.vm.network "private_network", ip: "192.168.101.14"
    v.vm.network "private_network", ip: "192.168.101.15"
    config.vm.provider :virtualbox do |vb|
      vb.customize ["modifyvm", :id, "--memory", "4096"]
    end
    v.vm.provision "ansible" do |ansible|
      ansible.playbook = "compact.yml"
      ansible.limit = "jira"
    end
  end

  config.vm.define "jenkins" do |v|
    v.vm.host_name = "jenkins"
    v.vm.network "private_network", ip: "192.168.101.16"
    v.vm.provider :virtualbox do |vb|
      vb.customize ["modifyvm", :id, "--memory", "1024"]
    end
    v.vm.provision "ansible" do |ansible|
      ansible.playbook = "compact.yml"
      ansible.limit = "jenkins"
    end
  end

  config.vm.define "elk" do |v|
    v.vm.host_name = "elk"
    v.vm.network "private_network", ip: "192.168.101.17"
    v.vm.network "private_network", ip: "192.168.101.18"
    v.vm.provider :virtualbox do |vb|
      vb.customize ["modifyvm", :id, "--memory", "3072"]
    end
    v.vm.provision "ansible" do |ansible|
      ansible.playbook = "compact.yml"
      ansible.limit = "elk"
    end
  end

end
