# bluetooth-monitor

bluetooth-monitor is a deamon listenning on incoming BT devices. 
It allows to execute a shell command on every device connection or disconnection , similar to what udev does.

# configuration File
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

# systemd Unit
in misc folder you can find a systemd unit , default config path for the unit is 

```
/etc/bluetooth-monitor/config.ini
```

