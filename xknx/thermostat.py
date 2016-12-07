from .device import Device
import time

class Thermostat(Device):
    def __init__(self, name, config):
        group_address = config["group_address"]
        Device.__init__(self)
        self.name = name
        self.group_address = group_address
        self.last_set = time.time();
        self.temperature = 0

    def get_name():
        return self.name

    def has_group_address(self, group_address):
        return self.group_address == group_address

    def process(self,telegram):
        if len(telegram.payload) != 3:
            raise(CouldNotParseSwitchTelegram)

        self.temperature = ( telegram.payload[1] * 256 + telegram.payload[2] ) / 100

        self.after_update_callback(self)

    def __str__(self):
        return "<Thermostat group_address={0}, name={1}>".format(self.group_address,self.name)
