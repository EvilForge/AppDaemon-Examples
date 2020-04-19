import appdaemon.plugins.hass.hassapi as hass
import datetime

#
# Humidity Control Shared Script
# 

#
# App to turn humidifiers on and off
#
# Use with constraints to activate only when a room isnt open to the outside.
#
# Args:
# sensor: Humidity sensor to use as trigger
# humidity_entity : entity to turn on or off
# high_limit: input_number.highhumidity
# low_limit: input_number.lowhumidity

# Declare Humidifier Control Class
class HumidifierControl(hass.Hass):
    def initialize(self):
        # Check some Params
        if "sensor" in self.args:
            self.handle = self.run_in(self.check_humidity, 300)
            self.log("Check {} in 300.".format(self.args["sensor"]))
        else:
            self.log("No sensor specified, doing nothing")

    def check_humidity(self, kwargs):
        pcthumid = self.get_state(self.args["sensor"])
        lowlimit = self.get_state(self.args["low_limit"])
        highlimit = self.get_state(self.args["high_limit"])
#        self.log("Humidity: {}%".format(pcthumid))
        if pcthumid < lowlimit and self.get_state(self.args["humidity_entity"])=="off":
#            self.log("Low Limit: {}".format(lowlimit))
#            self.log("Low humidity: turning {} on".format(self.args["humidity_entity"]))
            self.turn_on(self.args["humidity_entity"])
        if pcthumid > highlimit and self.get_state(self.args["humidity_entity"])=="on":
#            self.log("High Limit: {}".format(highlimit))
#            self.log("High humidity: turning {} off".format(self.args["humidity_entity"]))
            self.turn_off(self.args["humidity_entity"])
        self.cancel_timer(self.handle)
        self.handle = self.run_in(self.check_humidity, 300)
        self.log("Check {} in 300.".format(self.args["sensor"]))
