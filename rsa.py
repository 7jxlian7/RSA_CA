import random
import numpy as np

MIN = 100000
MAX = 1000000000

def generateKey():
    """Generate a pair of keys"""
    p = random.randint(MIN, MAX)
    q = random.randint(MIN, MAX)
    # On boucle jusqu'à ce que p et q soient premiers
    while(not isPrime(p) or not isPrime(q)):
        p = random.randint(MIN, MAX)
        q = random.randint(MIN, MAX)
    
    n = p * q
    phi = (p-1) * (q-1)

    # Génération de la clé publique
    e = random.randint(1, 1000) % (phi - 1) + 1 
    while(pgcd(e, phi) != 1):
        e = random.randint(1,1000)%(phi-1)+1
    
    # Génération de la clé privée
    d = bezout(e, phi)
    if d < 0:
        d += phi
    
    return [e, n, d]

def power(a, e, n):
    """exponentiation modulaire: calcule (a**b)%n"""
    p = 1
    while (e > 0) :
        if (e % 2 != 0) :
            p = (p * a) % n
        a = (a * a) % n
        e = e // 2
    return p

def pgcd(u, v):
    """Calculate the PGCD of u and v"""
    t = 0
    while (v):
        t = u
        u = v
        v = t % v
    return -u if u < 0 else u

def isPrime(n):
    if ((power(2,n-1,n)==1) and (power(3,n-1,n)==1) and (power(5,n-1,n)==1) and (power(7,n-1,n)==1) and (power(11,n-1,n)==1) and (power(13,n-1,n)==1)):
        return True #probablement premier (garantie si n<2^15)
    return False

def bezout(a, b):
    """Calculate x such as ax + by = 1 (mod b)"""
        # On sauvegarde les valeurs de a et b.
    a0 = a
    b0 = b
    # On laisse invariant p*a0 + q*b0 = a et  r*a0 + s*b0 = b.
    p = s = 1
    q = r = c = quotient = nouveau_r = nouveau_s = 0
    
    # La boucle principale.
    while (b != 0) :
        c = a % b
        quotient = a // b
        a = b
        b = c
        nouveau_r = p - quotient * r
        nouveau_s = q - quotient * s
        p = r
        q = s
        r = nouveau_r
        s = nouveau_s
    return p % b0

def generateKeys(i = 1):
    """Generate multiple keys"""
    keys = []
    for i in range(i):
        keys.append(generateKey())
    return keys