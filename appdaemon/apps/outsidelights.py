import appdaemon.plugins.hass.hassapi as hass
import datetime

#
# Outside Lighting App Shared Script
# 

#
# App to turn lights on and off at sunrise and sunset
#
# Args:
# on_scene: scene to activate at sunset
# off_scene: scene to activate at sunrise
#
# Declare Ambient Lighting Class
class NightLight(hass.Hass):
    def initialize(self):
        # Run at Sunrise
        self.run_at_sunrise(self.sunrise_cb)
        # Run at Sunset
        self.run_at_sunset(self.sunset_cb)

    def sunrise_cb(self, kwargs):
        self.log("OutsideLights: Sunrise Triggered")
        self.cancel_timers()
        self.turn_on(self.args["off_scene"])

    def sunset_cb(self, kwargs):
        self.log("OutsideLights: Sunset Triggered")
        self.cancel_timers()
        self.turn_on(self.args["on_scene"])

    def cancel_timers(self):
        if "timers" in self.args:
            apps = self.args["timers"].split(",")
            for app in apps:
                App = self.get_app(app)
                App.cancel()


#
# App to turn lights on when motion detected then off again after a delay
#
# Use with constraints to activate only for the hours of darkness
#
# Args:
# sensor: binary sensor to use as trigger
# entity_on : scene to turn on when detecting motion
# entity_off : scene to turn on when motion times out
# delay: amount of time after turning on to turn off again. If not specified defaults to 60 seconds.
#
# Declare Motion Lighting Class
class OutsideMotion(hass.Hass):
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
                delay = 180
            self.cancel_timer(self.handle)
            self.handle = self.run_in(self.light_off, delay)

    def light_off(self, kwargs):
        if "entity_off" in self.args:
            self.log("Motion timeout, Turning {} on".format(self.args["entity_off"]))
            self.turn_on(self.args["entity_off"])

    def cancel(self):
        self.cancel_timer(self.handle)
