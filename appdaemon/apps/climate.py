import appdaemon.plugins.hass.hassapi as hass
from datetime import datetime, time

#
# AC Temperature Control Shared Script
# 

#
# App to turn AC on and off
#
# Use with constraints to activate only between certain times. 5 minute checks because the AC unit needs that long to recover.
#
# Args:
# sensor: Humidity sensor to use as trigger
# entity_item : entity to turn on or off
# temperature: input_number.mbnighttemp
# start time, end_time : Time range to apply this temperature. HH:MM

# Declare AC Control Class
class ACControl(hass.Hass):
    def initialize(self):
        # Check some Params
        if "sensor" in self.args:
            self.run_in(self.check_time, 10)
            self.log("Check {} in 10s.".format(self.args["sensor"]))
        else:
            self.log("No sensor specified, doing nothing")

    def check_time(self, kwargs):
        # check for time limits. Skip control if outside limits, set callback to 2x.
        # within limits, control is every 5 minutes.
        begin = datetime.strptime(self.args["start_time"],"%H:%M").time()
        end = datetime.strptime(self.args["end_time"],"%H:%M").time()
        result = False
#        self.log("Now: {}".format(datetime.now().time()))
#        self.log("begin: {}".format(begin))
#        self.log("end: {}".format(end))
        if begin < end:
            if datetime.now().time() >= begin and datetime.now().time() <= end:
                result = True
        else: # crosses midnight
            if datetime.now().time() >= begin or datetime.now().time() <= end:
                result = True

        if result:
            self.run_in(self.check_time, 300)
            self.log("Active. Check {} in 300s.".format(self.args["sensor"]))
            airtemp = self.get_state(self.args["sensor"])
            setpoint = self.get_state(self.args["temperature"])
            self.log("Air temp: {}".format(airtemp))
            self.log("Set point: {}".format(setpoint))
            if airtemp > setpoint and self.get_state(self.args["entity_item"])=="off":
                self.log("High temp: turning {} on".format(self.args["entity_item"]))
                self.turn_on(self.args["entity_item"])
            if airtemp < setpoint and self.get_state(self.args["entity_item"])=="on":
                self.log("Low temp: turning {} off".format(self.args["entity_item"]))
                self.turn_off(self.args["entity_item"])
        else:
            self.run_in(self.check_time, 600)
            self.log("Inactive. Check {} in 600s.".format(self.args["sensor"]))
