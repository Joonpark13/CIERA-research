from exceptions import Exception

class parseExcept(Exception):
    def __init__(self, message=''):
        self.message = message
    def __str__(self):
        return self.message

class shortAlreadyExists(parseExcept):
    def __init__(self, message=''):
        self.message = message
    def __str__(self):
        return self.message
