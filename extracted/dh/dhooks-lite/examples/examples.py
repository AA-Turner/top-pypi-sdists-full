import datetime
import logging
import os

from dhooks_lite import Author, Embed, Field, Footer, Image, Thumbnail, Webhook

logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)

if "DISCORD_WEBHOOK_URL" not in os.environ:
    raise ValueError('mandatory environment variable "DISCORD_WEBHOOK_URL" not set')
else:
    DISCORD_WEBHOOK_URL = os.environ["DISCORD_WEBHOOK_URL"]


# Minimal example: Hello World
hook = Webhook(DISCORD_WEBHOOK_URL)
hook.execute("Hello, World!")

# Set username and avatar URL
hook = Webhook(
    DISCORD_WEBHOOK_URL,
    username="Bruce Wayne",
    avatar_url="https://i.imgur.com/thK8erv.png",
)
hook.execute("I am Batman!")

# Minmal embed example
hook = Webhook(DISCORD_WEBHOOK_URL)
e = Embed(description="Simple Embed example")
hook.execute(embeds=[e])


# Example with two embeds and all parameters
hook = Webhook(DISCORD_WEBHOOK_URL)
e1 = Embed(
    description="Only a few years ago, scientists stumbled upon an electrical current of cosmic proportions: 10^18 amps, or roughly one trillion lightning bolts. The lightning is thought to originate from an enormous black hole in the center of the galaxy, which has a core that is supposedly a “huge cosmic jet.” Apparently, the black hole’s huge magnetic field allows it to fire up this lightning bolt through gas and dust to a distance of over one hundred and fifty thousand light years away. And we thought that our galaxy was big, this single lightning bolt is one and a half times the size of it.",  # noqa
    title="Universe's highest electric current found",
    url="https://www.newscientist.com/article/mg21028174-900-universes-highest-electric-current-found/",  # noqa
    timestamp=datetime.datetime.now(),
    color=0x5CDBF0,
    footer=Footer("Science Department", "https://i.imgur.com/Bgsv04h.png"),
    image=Image("https://i.imgur.com/eis1Y0P.jpg"),
    thumbnail=Thumbnail("https://i.imgur.com/2A4k28x.jpg"),
    author=Author(
        "John Scientist",
        url="https://en.wikipedia.org/wiki/Albert_Einstein",
        icon_url="https://i.imgur.com/1JoHDw1.png",
    ),
    fields=[Field("1st Measurement", "Failed"), Field("2nd Measurement", "Succeeded")],
)
e2 = Embed(description="TOP SECRET - Do not distribute!")

response = hook.execute(
    "Checkout this new report from the science department:",
    username="Bruce Wayne",
    avatar_url="https://i.imgur.com/thK8erv.png",
    embeds=[e1, e2],
    wait_for_response=True,
)
print(response.headers)
print()
print(response.content)
