# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure('2') do |config|
  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine. In the example below,
  # accessing "localhost:8080" will access port 80 on the guest machine.
  # NOTE: This will enable public access to the opened port
  # config.vm.network "forwarded_port", guest: 80, host: 8080

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine and only allow access
  # via 127.0.0.1 to disable public access

  # Create a public network, which generally matched to bridged network.
  # Bridged networks make the machine appear as another physical device on
  # your network.
  # config.vm.network "public_network"

  # Share an additional folder to the guest VM. The first argument is
  # the path on the host to the actual folder. The second argument is
  # the path on the guest to mount the folder. And the optional third
  # argument is a set of non-required options.
  # config.vm.synced_folder "../data", "/vagrant_data"
  app_subnet = '192.168.70'
  lb_subnet = '192.168.50'
  db_subnet = '192.168.160'
  cluster_subnet = '192.168.150'
  iscsi_subnet = '192.168.140'

  N = 3
  (1..N).each do |node_id|
    config.vm.define "app-#{node_id}" do |node|
      config.vm.provider :libvirt do |libvirt|
        libvirt.memory = 2048
      end
      node.vm.box = 'generic/rocky8'
      node.vm.box_version = '3.6.8'
      node.vm.hostname = "app-#{node_id}"
      node.vm.network 'private_network', ip: "#{app_subnet}.#{20 + node_id}", netmask: '255.255.255.0'
      # Only execute the Ansible provisioner once, after all the nodes are up and ready.
      if node_id == N
        node.vm.provision :ansible do |ansible|
          # Disable default limit to connect to all the nodes
          ansible.groups = {
            'app' => ['app-1', 'app-2', 'app-3'],
            'lb' => ['lb-1'],
            'db' => ['db-1', 'db-2']
          }
          ansible.limit = 'all'
          ansible.playbook = 'provisioning/app.yml'
          ansible.host_vars = {
            'node1' => { 'testvar' => 'tk' }
          }
        end
      end
    end
  end

  (1..1).each do |node_id|
    config.vm.define "lb-#{node_id}" do |node|
      config.vm.provider :libvirt do |libvirt|
        libvirt.memory = 2048
      end
      node.vm.box = 'generic/rocky8'
      node.vm.box_version = '3.6.8'
      node.vm.hostname = "lb-#{node_id}"
      node.vm.network 'private_network', ip: "#{lb_subnet}.#{10 + node_id}", netmask: '255.255.255.0'
      node.vm.network 'private_network', ip: "#{app_subnet}.#{10 + node_id}", netmask: '255.255.255.0'
      node.vm.network 'forwarded_port', guest: 80, guest_ip: '192.168.70.11', host: 8080, host_ip: '127.0.0.1'
      # Only execute the Ansible provisioner once, after all the nodes are up and ready.
      node.vm.provision :ansible do |ansible|
        ansible.groups = {
          'lb' => ['lb-1']
        }
        # Disable default limit to connect to all the nodes
        ansible.limit = 'all'
        ansible.playbook = 'provisioning/lb.yml'
      end
    end
  end

  config.vm.define 'jumphost' do |node|
    config.vm.provider :libvirt do |libvirt|
      libvirt.memory = 2048
    end
    node.vm.box = 'generic/rocky8'
    node.vm.box_version = '3.6.8'
    node.vm.hostname = 'jumphost'
    node.vm.network 'private_network', ip: "#{lb_subnet}.99", netmask: '255.255.255.0'
    node.vm.network 'private_network', ip: "#{app_subnet}.99", netmask: '255.255.255.0'
    # Only execute the Ansible provisioner once, after all the nodes are up and ready.
    node.vm.provision :ansible do |ansible|
      ansible.groups = {
        'jumphost' => ['jumphost']
      }
      # Disable default limit to connect to all the nodes
      ansible.limit = 'all'
      ansible.playbook = 'provisioning/jumphost.yml'
    end
  end

  (1..2).each do |node_id|
    config.vm.define "db-#{node_id}" do |node|
      config.vm.provider :libvirt do |libvirt|
        libvirt.memory = 2048
      end
      node.vm.box = 'generic/rocky8'
      node.vm.box_version = '3.6.8'
      node.vm.hostname = "db-#{node_id}"
      node.vm.network 'private_network', ip: "#{db_subnet}.#{10 + node_id}", netmask: '255.255.255.0'
      node.vm.network 'private_network', ip: "#{app_subnet}.#{10 + node_id}", netmask: '255.255.255.0'
      node.vm.network 'private_network', ip: "#{cluster_subnet}.#{30 + node_id}", netmask: '255.255.255.0'
      node.vm.network 'private_network', ip: "#{iscsi_subnet}.#{30 + node_id}", netmask: '255.255.255.0'
      node.vm.provision :ansible do |ansible|
        ansible.groups = {
          'db' => ['db-1', 'db-2']
        }
        # Disable default limit to connect to all the nodes
        ansible.limit = 'all'
        ansible.playbook = 'provisioning/db.yml'
      end
    end
  end
end
