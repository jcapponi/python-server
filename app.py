# app.py
# Ejemplo simple de servidor REST con Flask.
# Este servidor permite crear, leer, actualizar y borrar textos usando HTTP.
# Los datos se guardan en memoria, por lo tanto se pierden al reiniciar el servidor.

from flask import Flask, request, jsonify  # Importa Flask y utilidades para manejar requests y respuestas JSON
from flask_cors import CORS  # Permite llamadas desde un frontend en otro origen

app = Flask(__name__)  # Crea la aplicación Flask
CORS(app)  # Habilita CORS para toda la app

texts_db = {}  # Diccionario global en memoria: {id: texto}


@app.route("/")  # Ruta principal
def home():
    return jsonify({  # Devuelve un JSON descriptivo
        "message": "Servidor REST funcionando",
        "endpoints": {
            "create": "POST /texts",
            "read": "GET /texts/<id>",
            "update": "PUT /texts/<id>",
            "delete": "DELETE /texts/<id>"
        }
    })


@app.route("/texts", methods=["POST"])  # Endpoint para crear un texto
def save_text():
    data = request.get_json()  # Lee el JSON enviado por el cliente

    if not data:  # Valida que haya JSON
        return jsonify({"error": "Debe enviar JSON"}), 400

    news_id = data.get("id")  # Obtiene el id
    text = data.get("text")  # Obtiene el texto

    if not news_id:  # Valida que exista el id
        return jsonify({"error": "El campo 'id' es obligatorio"}), 400

    if text is None:  # Valida que exista el texto
        return jsonify({"error": "El campo 'text' es obligatorio"}), 400

    if news_id in texts_db:  # Verifica que no exista repetido
        return jsonify({"error": f"Ya existe un texto con id '{news_id}'"}), 409

    texts_db[news_id] = text  # Guarda el texto en memoria

    return jsonify({  # Devuelve respuesta exitosa
        "message": "Texto guardado correctamente",
        "data": {
            "id": news_id,
            "text": text
        }
    }), 201


@app.route("/texts/<news_id>", methods=["GET"])  # Endpoint para leer un texto por id
def read_text(news_id):
    if news_id not in texts_db:  # Verifica que exista
        return jsonify({"error": f"No existe texto para id '{news_id}'"}), 404

    return jsonify({  # Devuelve el texto encontrado
        "message": "Texto recuperado correctamente",
        "data": {
            "id": news_id,
            "text": texts_db[news_id]
        }
    }), 200


@app.route("/texts/<news_id>", methods=["PUT"])  # Endpoint para actualizar un texto por id
def update_text(news_id):
    if news_id not in texts_db:  # Verifica que exista
        return jsonify({"error": f"No existe texto para id '{news_id}'"}), 404

    data = request.get_json()  # Lee el JSON enviado

    if not data:  # Valida que haya JSON
        return jsonify({"error": "Debe enviar JSON"}), 400

    text = data.get("text")  # Obtiene el nuevo texto

    if text is None:  # Valida que venga text
        return jsonify({"error": "El campo 'text' es obligatorio"}), 400

    texts_db[news_id] = text  # Actualiza el texto

    return jsonify({  # Devuelve respuesta de éxito
        "message": "Texto actualizado correctamente",
        "data": {
            "id": news_id,
            "text": text
        }
    }), 200


@app.route("/texts/<news_id>", methods=["DELETE"])  # Endpoint para borrar un texto por id
def delete_text(news_id):
    if news_id not in texts_db:  # Verifica que exista
        return jsonify({"error": f"No existe texto para id '{news_id}'"}), 404

    deleted_text = texts_db.pop(news_id)  # Borra el registro y guarda el texto borrado

    return jsonify({  # Devuelve confirmación
        "message": "Texto eliminado correctamente",
        "data": {
            "id": news_id,
            "deletedText": deleted_text
        }
    }), 200


if __name__ == "__main__":  # Se ejecuta solo si este archivo se corre directamente
    app.run(debug=True, port=5000)  # Inicia el servidor en modo debug en el puerto 5000