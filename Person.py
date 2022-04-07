import rsa

class Person:
    def __init__(self, name, id, keys):
        self.name = name
        self.id = id
        self.e = keys[0]
        self.n = keys[1]
        self.d = keys[2]
        self.certificat = 0
    def __str__(self):
        return "[{}] {}".format(self.id, self.name)
    def __repr__(self):
        return "[{}] {}".format(self.id, self.name)
    
    def getEmpreinte(self):
        return self.e + self.id * 5

    def encrypt(self, message, e, n):
        return rsa.power(message, e, n)
    
    def decrypt(self, message, e, n):
        return rsa.power(message, e, n)

    def setCertificat(self, n):
        self.certificat = n
    
    def getCertificat(self):
        return self.certificat