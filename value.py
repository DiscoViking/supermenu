import os

class EnvValue:
  def __init__(self, name):
    self.name = name

  def evaluate(self):
    return os.getenv(self.name)
