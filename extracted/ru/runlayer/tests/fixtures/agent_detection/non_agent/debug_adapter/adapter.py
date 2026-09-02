class DebugAdapter:
    def attach(self, client, address):
        client.connect(address)
