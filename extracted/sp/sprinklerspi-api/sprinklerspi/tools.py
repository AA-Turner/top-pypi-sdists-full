

OFFSET = 97

Z0 = 0
Z1 = 1
Z2 = 2

def get_url_zone_name(i): 
    return "z{}".format(chr(i+OFFSET))

def get_command(command):
    '''
    Get on or off string from integer 1 or 0
    '''
    if command:
        return 'on'
    else: 
        return 'off'