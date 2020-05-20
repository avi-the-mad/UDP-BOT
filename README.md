# UDP-BOT

## Network basics in esp-8266

Defining wifi station and access point. ESP8266 has both access point for devices to connect and wifi station for it to connect to wifi hotspots.
```
> import network
> sta_if = network.WLAN(network.STA_IF)
> ap_if = netwokr.WLAN(network.AP_IF)
```
