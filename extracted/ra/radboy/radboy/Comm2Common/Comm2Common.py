from . import *



'''
$PB=number selected from internal storage

sendlist pn - scan through Entries and send list data for selected list fields with inList==True to phonenumber
sendlist pb - scan through Entries and send list data for selected list fields with inList==True to $PB

send msg pn - send text msg to phonenumber
send msg pb - send text msg to $PB

process app text msg - process textual data recieved from texting app into useable data for radboy
    -ask if user wants to save to system or just view data sent
    
enable and init twilio api,eaita -enable twilio api and save api key

'''
class c2cm:
    def __init__(self):
        pass


    def sendmsg(self):
        FROM=Control(func=FormBuilderMkText,ptext="Phone Number FROM?",helpText="10 digit",data="string")
        if FROM is None:
            return
        to=Control(func=FormBuilderMkText,ptext="Phone Number to Send Msg to?",helpText="10 digit",data="string")
        if to is None:
            return

        msg=Control(func=FormBuilderMkText,ptext="Msg To Send: ",helpText="text message",data="string")
        if msg is None:
            return

        