import value

class Flag(object):
    """A flag represents a condition which must be satisfied for
    a menu item to be considered valid."""

    def isValid(self):
        """Whether this flag is considered valid.
        A menu item will only be considered valid if all of its
        flags are."""
        return True

class GenFlag(Flag):
    """A generic flag. Allows its validity to be decided by any arbitrary function of no arguments."""
    def __init__(self, function):
        self.isValid = function

class ValueFlag(Flag):
    """A flag whose validity is decided based on a value.
    It is deemed valid if the value matches the expected quantity.
    Or may be decided by a custom function which takes two arguments:
        1) The evaluated value
        2) The expected value
    e.g. custFunc = lambda a, b: a > b
    Will create a flag which is considered valid if the given value
    is greater than the expected quantity."""
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
    """A convenience class. Equivalent to a ValueFlag but specifically where
    the value is that of an environment variable."""
    def __init__(self, name, expect=None, custFunc=None):
        super(EnvFlag, self).__init__(value.EnvValue(name), expect, custFunc)
