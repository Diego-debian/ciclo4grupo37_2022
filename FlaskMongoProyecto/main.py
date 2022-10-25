from crypt import methods
import json
from flask import Flask, request, Response
from flask import jsonify
from flask_cors import CORS

from Controladores.CandidatoControlador import CandidatoControlador
from Controladores.PartidoControlador import PartidoControlador
from Controladores.MesaControlador import MesaControlador
from Controladores.ResultadoControlador import ResultadoControlador

app = Flask(__name__)
cors = CORS(app)

miControladorPartido = PartidoControlador()
miControladorCandidato = CandidatoControlador()
miControladorMesa = MesaControlador()
miControladorResultado = ResultadoControlador()

###########################################
###      Ruta de running servers        ###
###########################################
@app.route("/", methods=["GET"])
def test():
    json = {}
    json["message"] = "Server running ... :)"
    return jsonify(json)

###########################################
###      ENDPOINTS PARTIDOS             ###
###########################################
@app.route("/partidos", methods=["GET"])
def getPartidos():
    json = miControladorPartido.index()
    return jsonify(json)

@app.route("/partidos", methods=["POST"])
def crearPartido():
    data = request.get_json()
    json = miControladorPartido.create(data)
    return jsonify(json)

@app.route("/partidos/<string:id>", methods=["GET"])
def getPartido(id):
    json = miControladorPartido.show(id)
    return jsonify(json)

@app.route("/partidos/<string:id>", methods=["PUT"])
def modificarPartido(id):
    data = request.get_json()
    json = miControladorPartido.update(id, data)
    return jsonify(json)

@app.route("/partidos/<string:id>", methods=["DELETE"])
def eliminarPartido(id):
    json = miControladorPartido.delete(id)
    return jsonify(json)
    
if __name__ == "__main__":
    app.run(debug=False, port=9000)