from discord import SyncWebhook


class DiscordApiManager:
    """api manager for discord"""

    def send_msg(self, url, msg):
        webhook = SyncWebhook.from_url(url)
        webhook.send(msg)
