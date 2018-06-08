# bluetooth-monitor

bluetooth-monitor is a deamon listenning on incoming BT devices on Linux machine (it uses Bluez Dbus API).
It allows to execute a shell command on every device connection or disconnection , similar to what udev does.

# install
```
sudo pip install -r requirements.txt
```

# Usage
the daemon handles device already paired with the controller. In order to pair a device use
```
bluetoothctl
```

# configuration file
```
[AA:BB:CC:DD:EE:FF]
onconnect = 'echo hello >> /tmp/test'
ondisconnect = 'echo goodbye >> /tmp/test'
hci=hci0

[AF:FF:C1:DD:EE:FF]
onconnect = 'echo hello >> /tmp/test'
ondisconnect = 'echo goodbye >> /tmp/test'
hci=hci1
```

# systemd unit
in misc folder you can find a systemd unit , default config path for the unit is 

```
/etc/bluetooth-monitor/config.ini
```

