from itertools import product
from urllib import response
from flask import Flask, render_template, jsonify, request
from flask import Response, redirect, url_for
import database as dbase
from products import Products
from flask_cors import CORS

app = Flask(__name__)
db = dbase.dbConnection()
CORS(app)

#home
@app.route('/')
def home():
    return render_template('index.html')

#Método GET
@app.route('/get-products', methods=['GET'])
def getProduct():
    products = db['products']
    productsReceived = products.find()
    response = []
    for item in productsReceived:
        response.append(str(item))
    return jsonify(response)

#Método Post
@app.route('/post-products', methods=['POST'])
def addProduct():
    products = db['products']
    name = request.form['name']
    price = request.form['price']
    quantity = request.form['quantity']
    if name and price and quantity:
        product = Products(name, price, quantity)
        products.insert_one(product.toDBCollection())
        response = jsonify({
            'name': name,
            'price': price,
            'quantity': quantity
        })
        response.headers.add('Access-Control_Allow-Origin', '*')
        return redirect(url_for('home'))
    else:
        return notFound()

#método update
@app.route('/edit-product/<string:product_name>', methods=['POST'])
def editProduct(product_name):
    products = db['products']
    name = request.form['name']
    price = request.form['price']
    quantity = request.form['quantity']
    if name and price and quantity:
        products.update_one({'name':product_name},
        {'$set':{
            'name': name,
            'price': price,
            'quantity': quantity
        }})
        response = jsonify({
            'message': 'Producto ' + product_name + 'actualizado correctamente'
        })
        return redirect(url_for('home'))
    else:
        notFound()
        
#método delete
@app.route('/delete-product/<string:product_name>', methods=['DELETE'])
def delete(product_name):
    products = db['products']
    products.delete_one({
        'name': product_name
    })
    return redirect(url_for('home'))

#Errores
@app.errorhandler(404)
def notFound(error=None):
    message = {
        'message': 'No encontrado ' + request.url,
        'status': '404 not Found'
    }
    response = jsonify(message)
    response.status_code = 404
    response.headers.add('Access-Control_Allow-Origin', '*')
    return response

if __name__ == "__main__":
    app.run(debug=False, port= 4000)