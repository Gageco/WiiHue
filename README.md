# WiiHue
An attempt at making Hue Lights controllable with a wiimote.

## Table of Contents
* [Installation] (#installing)
* [Some Notes] (#notes)
* [Use] (#usage)

##Installing
Use the following command in terminal to install WiiHue
````
git clone https://github.com/Gageco/WiiHue
````

##Notes
- Some quick notes, only fifteen lights are supported at once due the only 4 leds on the wiimote and thats the limit of binary with the wiimote leds
- Make sure to install phue and cwiid these can be found here
- [phue](https://github.com/studioimaginaire/phue)
- [cwiid] (https://github.com/abstrakraft/cwiid)
The wiimote used needs to be one of the first ones with out the wiimotion plus inside

##Usage
To use you will need to find the ip of the Hue Bridge, make sure its on and the light bulbs are connected to it and copy the ip into the config file so at start up its automatically connected to. The wiimote is attached to the device at each start up so ensure that if the power goes out you reattach the remote.