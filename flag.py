import value

class Flag(object):
  def isValid(self):
    return True

class GenFlag(Flag):
  def __init__(self, function):
    self.isValid = function

class ValueFlag(Flag):
  def __init__(self, value, expect=None, custFunc=None):
    self.value = value
    self.expect = expect
    if custFunc != None:
      self.validate = custFunc
    else:
      self.validate = lambda a, b: a == b

  def isValid(self):
    try:
      return self.validate(self.value.evaluate(), self.expect)
    except:
      # Log failure.
      return False

class EnvFlag(ValueFlag):
  def __init__(self, name, expect=None, custFunc=None):
    super(EnvFlag, self).__init__(value.EnvValue(name), expect, custFunc)
