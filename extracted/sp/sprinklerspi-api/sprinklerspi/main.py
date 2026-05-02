import requests
import sprinklerspi.tools as tools

GET = 'GET'

class SprinklersPi(object): 

    def __init__(self, host, port = 8080): 
        self.host = host
        self.port = port 
        
    def get_url(self):
        return "http://{}:{}".format(self.host, self.port)

    def get_state(self): 
        '''
        Get state of the device
        '''
        req = requests.get("{}/json/state".format(self.get_url()))

        if req.ok: 
            return req.json()
        else:
            return []
    
    def get_zones(self): 
        '''
        Get running zones configuration
        '''
        req = requests.get("{}/json/zones".format(self.get_url()))

        if req.ok: 
            return req.json()['zones']
        else:
            return []

    def get_schedules(self): 
        '''
        Get schedules
        '''
        req = requests.get("{}/json/schedules".format(self.get_url()))

        if req.ok: 
            return req.json()['Table']
        else:
            return []

    def get_schedule(self, index): 
        '''
        Get a single schedule given its index
        '''
        req = requests.get("{}/json/schedule?id={}".format(self.get_url(), index))

        if req.ok: 
            return req.json()
        else:
            return []

    def switch_all_schedules(self, state): 
        req = requests.get("{}/bin/run?system={}".format(self.get_url(), tools.get_command(state)))

        return req.ok

    def switch_zone(self, zone, state):
        ''' 
        Switch zone one or off 
        1 for on 
        0 for off
        '''

        req = requests.get("{}/bin/manual?zone={}&state={}".format(self.get_url(), tools.get_url_zone_name(zone), tools.get_command(state)))

        return req.ok
        


    def set_zone(self, num, enabled, pump): 
        '''
        Set zone num to enable
        This is a little of a mess all the zone configuration, even previous ones shall be sent with the modified one ... TODO implement a logic to keep all this info
        ''' 
        pass

    





