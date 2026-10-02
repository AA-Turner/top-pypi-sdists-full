from discord_markdown import DEFAULT_FUEL, parse, unparse

print(parse("foo"))

# Ordinary content needs a tiny fraction of the default budget.
print(parse("**foo** _bar_", fuel=DEFAULT_FUEL))

# A budget too small for the content fails the parse outright; there is no partial AST.
try:
    parse("**foo**", fuel=1)
except Exception:
    print("parse ran out of fuel")
else:
    raise

# An AST goes back to the markdown it came from. Mention links are the reason this exists: the AST
# keeps the parsed resource, so the link cannot be rebuilt from it any other way.
for content in [
    "# Hello **world**",
    "https://discord.com/channels/1/2",
    "<@873227248453443624>",
]:
    assert unparse(parse(content)) == content, content
print("unparse round trips")

# A malformed AST is rejected rather than producing nonsense.
try:
    unparse([{"type": "nonsense"}])
except Exception:
    print("unparse rejects a malformed AST")
else:
    raise
