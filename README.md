XKNX
====

A Wrapper around KNX/UDP protocol written in python.

The wrapper is also intended to be used as a KNX logic module, which means to connect different KNX devices and make them interact.

At the moment the wrapper works with KNX/IP router.

Roadmap
-------

* Add functionality for KNX tunneling devices
* Add functionality for auto discovery for KNX/IP router and tunneling devices


Home-Assistant Plugin
---------------------

XKNX also contains a [Plugin](home-assistant-plugin) for the [Home-Assistant](https://home-assistant.io/) automation plattform

Supported / Tested Devices
--------------------------

The software was tested with the following devices:

- [GIRA KNX/IP-Routers 216700](http://www.gira.com/en/gebaeudetechnik/systeme/knx-eib_system/knx-produkte/systemgeraete/knx-ip-router.html)
- [GIRA KNX/Switching Actor  104000](http://katalog.gira.de/de_DE/deeplinking.html?artikelnr=104000&m=compare)
- [GIRA KNX/Shutter Binary Actor 103800](https://katalog.gira.de/en/datenblatt.html?id=635678)
- [GIRA KNX/Binary Input 111900 ](https://www.gira.de/gebaeudetechnik/systeme/knx-eib_system/knx-produkte/tasterschnittstellen/knxeib-universal-tasterschnittstelle.html)
- [GIRA Tastsensor 3 Plus 2-fach 514200 ](https://katalog.gira.de/de_DE/datenblatt.html?id=635019)
	(This sensor is also used as Thermostat)
- [KNX Dimmaktor 4fach](https://katalog.gira.de/de_DE/datenblatt.html?id=658701)

Sample Configuration
--------------------

```yaml
general:
    own_address: "15.15.249"
    own_ip: "192.168.42.1"

groups:

    switch:
        Livingroom.Switch1:
            group_address: 1025
            actions:
              - {hook: "off", switch_time: "long", target: Livingroom.Shutter_1, method: up}
              - {hook: "off", switch_time: "short", target: Livingroom.Shutter_1, method: short_up}

        Livingroom.Switch2:
            group_address: 1026
            actions:
              - {hook: "off", switch_time: "long", target: Livingroom.Shutter_1, method: down}
              - {hook: "off", switch_time: "short", target: Livingroom.Shutter_1, method: short_down}

        Livingroom.Switch3:
            group_address: 1027
            actions:
              - {hook: "on", target: Livingroom.Outlet_1, method: "on"}
              - {hook: "on", target: Livingroom.Outlet_2, method: "on"}
              - {hook: "on", target: Livingroom.Outlet_3, method: "on"}
              - {hook: "on", target: Livingroom.Outlet_4, method: "on"}

        Livingroom.Switch4:
            group_address: 1028
            actions:
              - {hook: "on", target: Livingroom.Outlet_1, method: "off"}
              - {hook: "on", target: Livingroom.Outlet_2, method: "off"}
              - {hook: "on", target: Livingroom.Outlet_3, method: "off"}
              - {hook: "on", target: Livingroom.Outlet_4, method: "off"}

    outlet:
        Livingroom.Outlet_1: {group_address: 65}
        Livingroom.Outlet_2: {group_address: 66}
        Livingroom.Outlet_3: {group_address: 67}
        Livingroom.Outlet_4: {group_address: 68}

    outlet 2:
        Kitchen.Outlet_1: {group_address: 12}
        Kitchen.Outlet_2: {group_address: 13}
        Kitchen.Outlet_3: {group_address: 14}
        Kitchen.Outlet_4: {group_address: 15}

    dimmer:
        Kitchen-L-1:     {group_address_switch: 332, group_address_dimm: 333, group_address_dimm_feedback: 334}
        Dining-Room-L-1: {group_address_switch: 335, group_address_dimm: 336, group_address_dimm_feedback: 337}
        Stairs-L-1:      {group_address_switch: 338, group_address_dimm: 339, group_address_dimm_feedback: 340}
        Living-Room-L-1: {group_address_switch: 341, group_address_dimm: 342, group_address_dimm_feedback: 343}

    shutter:
        Central.Shutter: {group_address_long: 3073 }

        Livingroom.Shutter_1: {group_address_long: 3171, group_address_short: 3172, group_address_position_feedback: 3173, group_address_position: 3174}
        Livingroom.Shutter_2: {group_address_long: 3175, group_address_short: 3176, group_address_position_feedback: 3177, group_address_position: 3178}

    thermostat:
        Kitchen.Thermostat_1: {group_address: 2049}
```

Basic Operations
----------------

```python

# Outlet

devices_.device_by_name("Livingroom.Outlet_1").set_on()
time.sleep(5)
devices_.device_by_name("Livingroom.Outlet_2").set_off()

# Shutter
devices_.device_by_name("Livingroom.Shutter_1").set_down()
time.sleep(2)
devices_.device_by_name("Livingroom.Shutter_1").set_up()
time.sleep(5)
devices_.device_by_name("Livingroom.Shutter_1").set_short_down()
time.sleep(5)
devices_.device_by_name("Livingroom.Shutter_1").set_short_up()

```


Sample Program
--------------

```
#!/usr/bin/python3
from xknx import Multicast,Devices,devices_,Config

Config.read()
Multicast().recv()
```

`Multicast().recv()` may also take a callback as parameter:

```python
#!/usr/bin/python3

from xknx import Multicast,CouldNotResolveAddress,Config
import time

def callback( device, telegram):

    print("Callback received from {0}".format(device.name))

    try:

        if (device.name == "Livingroom.Switch_1" ):
            if device.is_on():
                devices_.device_by_name("Livingroom.Outlet_1").set_on()
            elif device.is_off():
                devices_.device_by_name("Livingroom.Outlet_1").set_off()

    except CouldNotResolveAddress as c:
        print(c)

Config.read()
Multicast().recv(callback)
```
