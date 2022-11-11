from flask import Flask, jsonify, request
from flask_cors import CORS
from waitress import serve
import datetime
import requests
import re
import json

app = Flask(__name__)
cors = CORS(app)

from flask_jwt_extended import create_access_token, verify_jwt_in_request
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

######################################
##    CREAR TOKEN O MÉTODO LOGIN    ##
######################################
app.config["JWT_SECRET_KEY"]='super-secret' #puedes colocar la contraseña que quieras
jwt = JWTManager(app)

@app.route("/login", methods=['POST'])
def create_token():
    data = request.get_json()
    headers = {"Content-Type": "application/json; charset=utf-8"}
    url = dataConfig["url-backend-security"]+"/usuarios/validar"
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        user = response.json()
        expires = datetime.timedelta(seconds=60*60*24)#Un día en segundos
        access_token = create_access_token(identity=user,
            expires_delta=expires)
        return jsonify({"token": access_token,
            "user_id":user["_id"]
        })
    else:
        return jsonify({
            "Message": "correo, seudonimo o contraseña incorrecta"
        }), 401

######################################
##    Implementación middleware     ##
######################################
def limpiarURL(url):
    partes = request.path.split("/")
    for laParte in partes:
        if re.search('\\d', laParte):
            url = url.replace(laParte, "?")
        return url

def validarPermiso(endPoint, metodo, idRol):
    url=dataConfig["url-backend-security"]+"/permisos-roles/validar-permiso/rol/"+str(idRol)
    tienePermiso=False
    headers = {"Content-Type": "application/json; charset=utf-8"}
    body={
        "url":endPoint,
        "metodo":metodo
        }
    response = requests.get(url,json=body, headers=headers)
    try:
        data=response.json()
        if("_id" in data):
            tienePermiso=True
    except:
        pass
    return tienePermiso

@app.before_request
def before_request_callback():
    endPoint=limpiarURL(request.path)
    excludedRoutes=["/login"]
    if excludedRoutes.__contains__(request.path):
        print("ruta excluida ",request.path)
        pass
    elif verify_jwt_in_request():
        usuario = get_jwt_identity()
        if usuario["rol"]is not None:
            tienePersmiso=validarPermiso(endPoint,request.method,usuario["rol"]["_id"])
            if not tienePersmiso:
                return jsonify({"message": "Permission denied"}), 401    
        else:
            return jsonify({"message": "Permission denied"}), 401

######################################
##        ENDPOINTS DE MESAS        ##
######################################
@app.route("/mesas", methods=['GET'])
def getMesas():
    headers= {"Content-Type": "application/json; charset=utf-8"}
    url = dataConfig["url-backend-votes"]+'/mesas'
    response = requests.get(url, headers=headers)
    Json = response.json()
    return jsonify(Json)

@app.route("/mesas", methods=["POST"])
def crearMesas():
    data = request.get_json() #Para los datos que llegan en el body
    headers= {"Content-Type": "application/json; charset=utf-8"}
    url = dataConfig["url-backend-votes"]+'/mesas'
    response = requests.post(url, headers=headers, json=data)
    Json = response.json()
    return jsonify(Json)

@app.route("/mesas/<string:id>", methods=['GET'])
def getMesa(id):
    headers= {"Content-Type": "application/json; charset=utf-8"}
    url = dataConfig["url-backend-votes"]+'/mesas/'+id
    response = requests.get(url, headers=headers)
    Json = response.json()
    return jsonify(Json)

@app.route("/mesas/<string:id>", methods=["PUT"])
def modificarMesas(id):
    data = request.get_json() #Para los datos que llegan en el body
    headers= {"Content-Type": "application/json; charset=utf-8"}
    url = dataConfig["url-backend-votes"]+'/mesas/'+id
    response = requests.put(url, headers=headers, json=data)
    Json = response.json()
    return jsonify(Json)

@app.route("/mesas/<string:id>", methods=['DELETE'])
def eliminarMesa(id):
    headers= {"Content-Type": "application/json; charset=utf-8"}
    url = dataConfig["url-backend-votes"]+'/mesas/'+id
    response = requests.get(url, headers=headers)
    Json = response.json()
    return jsonify(Json)

######################################
##      ENDPOINTS DE PARTIDOS       ##
######################################
@app.route("/partidos", methods=['GET'])
def getPartidos():
    headers= {"Content-Type": "application/json; charset=utf-8"}
    url = dataConfig["url-backend-votes"]+'/partidos'
    response = requests.get(url, headers=headers)
    Json = response.json()
    return jsonify(Json)

@app.route("/partidos", methods=["POST"])
def crearPartidos():
    data = request.get_json() #Para los datos que llegan en el body
    headers= {"Content-Type": "application/json; charset=utf-8"}
    url = dataConfig["url-backend-votes"]+'/partidos'
    response = requests.post(url, headers=headers, json=data)
    Json = response.json()
    return jsonify(Json)

@app.route("/partidos/<string:id>", methods=['GET'])
def getPartido(id):
    headers= {"Content-Type": "application/json; charset=utf-8"}
    url = dataConfig["url-backend-votes"]+'/partidos/'+id
    response = requests.get(url, headers=headers)
    Json = response.json()
    return jsonify(Json)

@app.route("/partidos/<string:id>", methods=["PUT"])
def modificarPartido(id):
    data = request.get_json() #Para los datos que llegan en el body
    headers= {"Content-Type": "application/json; charset=utf-8"}
    url = dataConfig["url-backend-votes"]+'/partidos/'+id
    response = requests.put(url, headers=headers, json=data)
    Json = response.json()
    return jsonify(Json)

@app.route("/partidos/<string:id>", methods=['DELETE'])
def eliminarMesa(id):
    headers= {"Content-Type": "application/json; charset=utf-8"}
    url = dataConfig["url-backend-votes"]+'/partidos/'+id
    response = requests.get(url, headers=headers)
    Json = response.json()
    return jsonify(Json)

######################################
##     TEST O PRUEBA DE SERVICIO    ##
######################################
@app.route("/", methods=['GET'])
def test():
    #variable de paso
    Json = {}
    Json["Message"] = "Server Running ..."
    return jsonify(Json)

def loadFileConfig():
    with open('config.json') as f:
        data = json.load(f)
    return data

if __name__ == "__main__":
    dataConfig = loadFileConfig()
    print("Server rurl-backend running : http://"+ 
        dataConfig["url-backend"]+ ":"+
        dataConfig["port"])
    serve(app, host=dataConfig["url-backend"], 
        port=dataConfig["port"])