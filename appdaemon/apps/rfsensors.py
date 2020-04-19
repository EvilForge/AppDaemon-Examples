import appdaemon.plugins.hass.hassapi as hass

#
# RF Sensor Processing Shared Script
# 

#
# App to set room open or closed after delay. Uses Hass input_boolean to mark a room closed.
#
# Args:
# sensor: binary sensor(s) to use as trigger
# entity_closed : boolean input that marks a room as 'closed' when on.
# delay: amount of time after door being open causes room to set from 'closed' to 'open'.
#
# Declare Door Watching Class
class WatchDoor(hass.Hass):
    def initialize(self):
        self.handle = None
        # Subscribe to sensors - open needs to be open for delay, closed is quicker reaction.
        for entry in self.args["sensor"]:
            self.log("callback for {}".format(entry))
            self.handle = self.listen_state(self.left_open, entry["entity"], new = "on")
            self.handle = self.listen_state(self.closed, entry["entity"], new = "off")
            self.handle = self.listen_state(self.left_open, entry["entity"], new = "on", duration = self.args["delay"])
            self.handle = self.listen_state(self.closed, entry["entity"], new = "off", duration = 5)

    def left_open(self, entity, attribute, old, new, kwargs):
        allopen = True
        for entry in self.args["sensor"]:
            self.log("Checking door {}".format(entry))
            sensstate = self.get_state(entry["entity"],attribute="state")
            self.log("door is {}".format(sensstate))
            if sensstate == "off":
                self.log("All doors are not open. {}".format(entry))
                allopen = False
        if allopen:
            self.log("Left open: {}".format(self.args["sensor"]))
            self.log("Setting {} to open".format(self.args["entity_closed"]))
            self.turn_off(self.args["entity_closed"])

    def closed(self, entity, attribute, old, new, kwargs):
        anyclosed = False
        for entry in self.args["sensor"]:
            self.log("Checking door {}".format(entry))
            sensstate = self.get_state(entry["entity"],attribute="state")
            if sensstate == "on":
                self.log("At least one door is closed. {}".format(entry))
                anyclosed = True
        if anyclosed:
            self.log("Closed: {}".format(self.args["sensor"]))
            self.log("Setting {} to closed".format(self.args["entity_closed"]))
            self.turn_on(self.args["entity_closed"])


#
# App to toggle entity(ies) when a RF switch plate button is pressed. Simple On Off.
#
# Args:
# sensor: binary sensor to use as trigger
# entity_item : Entities to turn on and off
#
# Declare plate switch Class
class PlateSwitch(hass.Hass):
    def initialize(self):
        self.handle = None
        # Subscribe to sensors
        if "sensor" in self.args:
            for entry in self.args["sensor"]:
#                self.log("callback for {}".format(entry["entity"]))
                self.handle = self.listen_state(self.toggle, entry["entity"], new = "on")
        else:
            self.log("No sensor specified, doing nothing")

    def toggle(self, entity, attribute, old, new, kwargs):
        for entry in self.args["entity_item"]:
#            self.log("Toggle {}".format(entry["entity"]))
            entstate = self.get_state(entry["entity"],attribute="state")
            if entstate == "on":
#                self.log("Turning Off {}".format(entry["entity"]))
                self.turn_off(entry["entity"])
            else:
#                self.log("Turning On {}".format(entry["entity"]))
                self.turn_on(entry["entity"])

