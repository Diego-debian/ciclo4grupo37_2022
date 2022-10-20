from pymongo import MongoClient
import certifi
#conexión a mongo local
MONGO_URI = "mongodb://localhost"
PORT = 27017

#conexión a mongo remota
MONGO_URI = "mongodb+srv://Ciclo4Grupo37:Ciclo4Grupo37@cluster0.9uen0xp.mongodb.net/?retryWrites=true&w=majority"
ca = certifi.where()

def dbConnection():
    try:
        #Conexión Local
    #    client = MongoClient(MONGO_URI, port=PORT)
        #conexión remota
        client = MongoClient(MONGO_URI, tlsCAFile=ca)
        db = client["ciclo4_grupo37_db"]
    except:
        print("Error en la conexión a la DB")
    return db