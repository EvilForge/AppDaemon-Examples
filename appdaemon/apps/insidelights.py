import appdaemon.plugins.hass.hassapi as hass
import datetime

#
# Outside Lighting App Shared Script
# 

#
# App to turn lights on when motion detected then off again after a delay
#
# Use with constraints to activate only for the hours of darkness
#
# Args:
# sensor: binary sensor to use as trigger
# entity_on : entity to turn on when detecting motion, can be a light, script, scene or anything else that can be turned on
# entity_off : entity to turn off when detecting motion, can be a light, script or anything else that can be turned off. Can also be a scene which will be turned on
# delay: amount of time after turning on to turn off again. If not specified defaults to 60 seconds.
#
# Declare Motion Lighting Class
class InsideMotion(hass.Hass):
    def initialize(self):
        self.handle = None
        # Check some Params
        # Subscribe to sensors
        if "sensor" in self.args:
            self.listen_state(self.motion, self.args["sensor"])
        else:
            self.log("No sensor specified, doing nothing")

    def motion(self, entity, attribute, old, new, kwargs):
        if new == "on":
            if "entity_on" in self.args:
                self.log("Motion detected: turning {} on".format(self.args["entity_on"]))
                self.turn_on(self.args["entity_on"])
            if "delay" in self.args:
                delay = self.args["delay"]
            else:
                delay = 60
            self.cancel_timer(self.handle) # cancel existing timer if it exists, set a new one.
            self.handle = self.run_in(self.light_off, delay)

    def light_off(self, kwargs):
        if "entity_off" in self.args:
            self.log("Motion timeout, turning {} on".format(self.args["entity_off"]))
            self.turn_on(self.args["entity_off"])

    def cancel(self):
        self.cancel_timer(self.handle)

#
# App to turn off idle light after delay.
#
# Args:
# entity_watched : Switch(es) or item(s) to watch.
# delay: amount of time after no activity that item is turned off.
#
# Declare Light Watching Class
class IdleLight(hass.Hass):
    def initialize(self):
        self.handle = None
        if "delay" in self.args:
            delay = self.args["delay"]
        else:
            delay = 60        # Subscribe to sensors - open needs to be open for delay, closed is quicker reaction.
        for entry in self.args["entity_watched"]:
            self.log("callback for {}".format(entry["entity"]))
            self.handle = self.listen_state(self.left_open, entry["entity"], new = "on", duration = delay)

    def left_open(self, entity, attribute, old, new, kwargs):
        for entry in self.args["entity_watched"]:
            self.log("Turning off {}".format(entry["entity"]))
            self.turn_off(entry["entity"])
