import os

class EnvValue:
    """Represents an environment variable."""
    def __init__(self, name):
        self.name = name

    def evaluate(self):
        """Evalutate the value of this value."""
        return os.getenv(self.name)
