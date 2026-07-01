from discord_markdown import CancelToken, parse

print(parse("foo"))

cancel_token = CancelToken()
cancel_token.cancel()
try:
    parse("foo", cancel_token=cancel_token)
except:
    print("parse canceled")
else:
    raise
