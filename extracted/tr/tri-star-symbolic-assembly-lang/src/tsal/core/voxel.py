class MeshVoxel:
    """Universal symbolic data point: pace, rate, state, spin."""

    def __init__(self, pace, rate, state, spin):
        self.pace = pace
        self.rate = rate
        self.state = state
        self.spin = spin

    def as_dict(self):
        return {
            "pace": self.pace,
            "rate": self.rate,
            "state": self.state,
            "spin": self.spin,
        }
