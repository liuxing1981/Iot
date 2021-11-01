# Iot 

## Install EMQ X mqtt
```buildoutcfg
curl https://repos.emqx.io/install_emqx.sh | bash
gui http://127.0.0.1:18083/#/plugins
admin/public
start meesia
sudo emqx stop
vi /etc/emqx/plugins/emqx_auth_mnesia.conf
sudo emqx start
```

## Install python package
```buildoutcfg
sudo -E python3 -m pip install paho-mqtt
sudo -E python3 -m pip install taospy
```

## Install TDengine
```buildoutcfg
wget https://www.taosdata.com/assets-download/TDengine-server-2.0.20.13-Linux-x64.rpm
sudo yum install TDengine-server-2.0.20.13-Linux-x64.rpm
alter user root pass siemens!123
```

## Install Grafana
```buildoutcfg
wget https://dl.grafana.com/enterprise/release/grafana-enterprise-7.0.0-1.x86_64.rpm
sudo yum install grafana-enterprise-7.0.0-1.x86_64.rpm
systemctl status grafana-server
sudo sed -i 's/.*allow_loading_unsigned_plugins.*/allow_loading_unsigned_plugins = taosdata-tdengine-datasource/' /etc/grafana/grafana.ini
sudo cp -r /usr/local/taos/connector/grafanaplugin /var/lib/grafana/plugins/

select avg(speed)  from db_0532_01.device01 WHERE ts>=$from and ts<$to interval($interval)
```