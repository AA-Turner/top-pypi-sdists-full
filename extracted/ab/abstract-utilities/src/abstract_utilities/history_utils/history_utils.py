class HistoryManager:
    def __init__(self):
        self.history_names = {}

    def add_history_name(self, name, initial_data=''):
        self.history_names[name] = {"history": [initial_data], "history_redo": []}
        return name

    def transfer_state(self, primary_data, secondary_data):
        """
        Transfer the latest state from primary_data to secondary_data
        Returns the modified primary and secondary data lists
        """
        self.last_data = None
        # If there's data in primary, transfer the latest to secondary
        if primary_data:
            self.last_data = primary_data.pop()
            secondary_data.append(self.last_data)

        return primary_data, secondary_data

    def add_to_history(self, name, data):
        # Clear the redo history when a new state is added
        self.history_names[name]['history_redo'] = []
        self.history_names[name]['history'].append(data)

    def redo(self, name):
        # Redo by transferring state from redo history to actual history
        self.history_names[name]["history_redo"], self.history_names[name]["history"] = self.transfer_state(
            self.history_names[name]["history_redo"], self.history_names[name]["history"])
        return self.last_data

    def undo(self, name):
        # Undo by transferring state from actual history to redo history
        self.history_names[name]["history"], self.history_names[name]["history_redo"] = self.transfer_state(
            self.history_names[name]["history"], self.history_names[name]["history_redo"])
        return self.last_data
