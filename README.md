# WiiHue
An attempt at making Hue Lights controllable with a wiimote.

## Table of Contents
* [Installation](#installing)
* [Some Notes](#notes)
* [Use](#usage)
* [Key Bindings](#bindings)
* [Future Plans](#plans)

## Installing
Use the following command in terminal to install WiiHue
````
git clone https://github.com/Gageco/WiiHue
````

## Notes
- Some quick notes, only fifteen lights are supported at once due the only 4 leds on the wiimote and thats the limit of binary with the wiimote leds
- Make sure to install phue and cwiid these can be found here
- [phue](https://github.com/studioimaginaire/phue)
- [cwiid](https://github.com/abstrakraft/cwiid)

  The wiimote used needs to be one of the first ones with out the wiimotion plus inside or else cwiid wont work

## Usage
To use you will need to find the ip of the Hue Bridge, make sure its on and the light bulbs are connected to it and copy the ip into the config file so at start up its automatically connected to. The wiimote is attached to the device at each start up so ensure that if the power goes out you reattach the remote.

## Bindings
|Key| Function           
|---|
|A| Toggle individual light states
|B| Check light state, blinks once for off twice for on
|Up Arrow| Choose next light
|Down Arrow| Choose previous light     
|Left Arrow| Increase brightness of individual light
|Right Arrow| Decrease brightness of individual light
|1 Button| Toggle room one lights
|2 Button| Toggle room two lights
|Home| Manual Disconnect

## Plans
Some things I want to add in the future
- [x] Feedback for getting the state of the light possibly using the B buttons
- [ ] More Rooms
- [ ] Low Battery Disconnect
- [x] Manual Disconnect
