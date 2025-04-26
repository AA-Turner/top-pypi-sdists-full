from helpscout import HelpScout


app_id = 'ec16a19f9fa84f8691b07f08ec52c0e4'
app_secret = '81f53e35ff164489979d4182be1d5385'
conversation_id = 941637666
hs = HelpScout(app_id, app_secret)
# threads = hs.conversations[conversation_id].threads.get()
cs = hs.conversations
ci = cs[conversation_id]
th = ci.threads

# print(hs.hit('mailboxes', 'get'))

conversation_id = 958227636
ci = cs[conversation_id]
