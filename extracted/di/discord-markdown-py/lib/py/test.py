from discord_markdown import DEFAULT_FUEL, Syntax, parse, unparse

print(parse("foo"))

# Every syntax is on by default.
assert parse("**foo**") == [{"type": "paragraph", "value": [{"type": "bold", "value": [{"type": "text", "value": "foo"}]}]}]

# `flags` turns syntax on by bit, and a mask turns it off.
assert parse("**foo** _bar_", flags=Syntax.UNDERSCORE_ITALIC) == [
    {
        "type": "paragraph",
        "value": [
            {"type": "text", "value": "**foo** "},
            {"type": "italic", "value": [{"type": "text", "value": "bar"}]},
        ],
    }
]
assert parse("@everyone", flags=Syntax.ALL & ~Syntax.MENTIONS) == [
    {"type": "paragraph", "value": [{"type": "text", "value": "@everyone"}]}
]
# no flags at all would be plain text, so zero means everything
assert parse("**foo**", flags=0) == parse("**foo**")
print("flags select syntax")

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
