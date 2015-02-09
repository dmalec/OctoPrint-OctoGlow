OctoGlow Plugin
===============

This is a plugin for displaying [OctoPrint](http://octoprint.org/) status on a [Pimoroni PiGlow](http://shop.pimoroni.com/products/piglow).

In addition to installing the plugin, you will need to enable i2c on your Raspberry Pi.

Requirements
------------
* Raspberry Pi
* Pimoroni PiGlow
* OctoPi 1.2.0+

Acknowledgements
----------------
OctoGlow uses Jason Barnett's [PiGlow Python module](https://github.com/Boeeerb/PiGlow)

Enabling i2c
------------
The PiGlow board requires i2c to be enabled on the Raspberry Pi.  Please follow the [Pimoroni guide on enabling i2c](https://github.com/pimoroni/piglow) on the Raspberry Pi.

Additionally, the pi user must be added to the i2c group in order to allow OctoPrint to send commands to the PiGlow without needing root privileges:
``` bash
sudo adduser pi i2c
```

Moving to OctoPrint 1.2.0
-------------------------
Follow the process in [the OctoPrint FAQ](https://github.com/foosel/OctoPrint/wiki/FAQ#how-can-i-switch-the-branch-of-the-octoprint-installation-on-my-octopi-image) to move to the development branch

Installing the Plugin
---------------------
Install the plugin like you would install any regular Python package from source:

``` bash
pip install https://github.com/dmalec/OctoPrint-OctoGlow/archive/master.zip
```

Make sure you use the same Python environment that you installed OctoPrint under, otherwise the plugin won't be able to satisfy its dependencies.

