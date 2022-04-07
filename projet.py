import Person as p
import rsa
import time

def main():
    # Generate 3 paris of keys
    keys = rsa.generateKeys(3)

    # Create 3 persons
    Alice = p.Person("Alice", 3108, keys[0])
    Bob = p.Person("Bob", 2002, keys[1])
    Ca = p.Person("CA", 1234, keys[2])

    # Alice wants to authenticate to CA
    empreinte_alice = Alice.getEmpreinte()

    # Son message est sa clé publique avec son empreinte
    message = str(Alice.e) + "," + str(empreinte_alice)
    print(">> Clé publique d'Alice :", Alice.e)
    time.sleep(2)
    print(">> Empreinte d'Alice :", empreinte_alice)
    time.sleep(2)

    # On chiffre la clé publique d'Alice avec la clé publique du CA
    chiffred_pk = Alice.encrypt(Alice.e, Ca.e, Ca.n)

    # On chiffre l'empreinte de Alice avec sa clé privée et la clé publique du CA
    chiffred_empreinte = Alice.encrypt(empreinte_alice, Alice.d, Alice.n)
    chiffred_empreinte = Alice.encrypt(chiffred_empreinte, Ca.e, Ca.n)

    print(">> Clé publique chiffrée d'Alice :", chiffred_pk)
    time.sleep(2)
    print(">> Empreinte chiffrée d'Alice :", chiffred_empreinte)
    time.sleep(2)

    sendMessage([chiffred_pk, chiffred_empreinte], Ca)

    # Le CA reçoit le message
    pk_received = Ca.decrypt(chiffred_pk, Ca.d, Ca.n)

    empreinte_received = Ca.decrypt(chiffred_empreinte, Ca.d, Ca.n)
    empreinte_received = Ca.decrypt(empreinte_received, pk_received, Alice.n)

    print("Clé publique reçue :", pk_received)
    print("Empreinte reçue :", empreinte_received)

    # Si on a reçu la bonne empreinte, alors on peut valider le certificat
    if empreinte_received == empreinte_alice:
        print("Authentification réussie !")
        time.sleep(3)
        certificat = Ca.encrypt(Alice.e, Ca.d, Ca.n)
        Alice.setCertificat(certificat)
    else:
        print("Authentification échouée !")
        return
    
    if Alice.getCertificat() != 0:
        sendMessage(certificat, Bob)

        certificat_received = Bob.decrypt(Alice.getCertificat(), Ca.e, Ca.n)

        # Si mon certificat déchiffré est correct
        if (certificat_received == Alice.e):
            print("Certificat vérifié !")
            
            # Bob envoie un message à Alice
            messageBob = 987654321
            chiffred_messageBob = Bob.encrypt(messageBob, certificat_received, Alice.n)
            sendMessage(chiffred_messageBob, Alice)

            # Alice a reçu le message
            messageBob_received = Alice.decrypt(chiffred_messageBob, Alice.d, Alice.n)
            print(">> Alice a reçu le messsage : " + str(messageBob_received) + " de Bob (original : " + str(messageBob) + ")")
        


def sendMessage(message, target):
    print("Message [{msg}] en cours de transmission à {dest}".format(msg=message, dest=target.name))
    for i in range(0, 3):
        print(".")
        time.sleep(1)
    print("Message envoyé")

main()