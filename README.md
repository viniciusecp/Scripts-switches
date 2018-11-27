Scripts Switches
================

O script show-vlan.py é necessário instalar o pacote python3-tk utilizado para interface gráfica.

Os arquivos ansible.cfg, inventory e os tres com extensão yml, são os arquivos do ansible, sendo que foi criado três scrips ansible, cada um para um tipo de switch, dell, ios e nexus.

O script show-vlan.py normaliza os arquivos e apresenta todas as vlans existentes no switch entre a vlan x e y informadas, este apresenta uma interface gráfica.

O script show-vlan-range.py normaliza os arquivos e apresenta todas as vlans informadas no arquivo csv, este apresenta apenas interface do terminal.

Dentro da pasta web-interface está o sistema funcionando com uma interface web utilizando o flask. Nela foi implementado o script show-vlan-range.
