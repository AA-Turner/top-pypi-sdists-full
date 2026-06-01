# utils/warnings.py
class WarningCollector:
    def __init__(self):
        self.warnings = []

    def add(self, message: str):
        if message not in self.warnings:
            self.warnings.append(message)

    def has_warnings(self) -> bool:
        return bool(self.warnings)

    def show(self):
        if self.warnings:
            print("\nWarnings:")
            for w in self.warnings:
                print("- ", w.encode('utf-8'))

    def export(self, filepath: str = "warnings.txt"):
        with open(filepath, "w", encoding="utf-8") as f:
            for w in self.warnings:
                f.write(f"- {w}\n")
