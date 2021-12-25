import json
import sqlite3

from flask import Flask, jsonify, request, Response
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

conn = sqlite3.connect(r"ChristmasGifts.db", check_same_thread=False)
c = conn.cursor()
c.execute(
    """
    CREATE TABLE IF NOT EXISTS ChristmasGifts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name text,
        price text,
        number text
        )
    """
)
conn.commit()
c.close()


def to_response(data, message, code):
    response = {
        "result": data,
        "error": None,
        "message": message
    }
    return Response(json.dumps(response), status=code, mimetype="application/json")


def to_error_response(error, message, code=500):
    response = {
        "result": None,
        "error": error,
        "message": message
    }
    return Response(json.dumps(response), status=code, mimetype="application/json")


@app.route('/api/v1/ChristmasGifts', methods=['GET'])
def get_ChristmasGifts_list():
    c1 = conn.cursor()
    query = "select * from ChristmasGifts"
    c1.execute(query)
    results = c1.fetchall()
    ChristmasGifts_list = []
    for result in results:
        ChristmasGifts_list.append({
            "id": result[0],
            "name": result[1],
            "price": result[2],
            "number": result[3]

        })
    return to_response(ChristmasGifts_list, "ChristmasGifts list loaded", 200)


@app.route('/api/v1/ChristmasGifts/<int:id>', methods=['GET'])
def get_ChristmasGifts_by_id(id):
    try:
        c1 = conn.cursor()
        query = "select * from ChristmasGifts where id = :id"
        c1.execute(query, {"id": id})
        result = c1.fetchone()
        founded_ChristmasGifts = {
            "id": result[0],
            "name": result[1],
            "price": result[2],
            "number": result[3]
        }
        return to_response(founded_ChristmasGifts, "ChristmasGifts loaded", 200)
    except sqlite3.Error as err:
        return to_error_response(' '.join(err.args), "", 500)


@app.route('/api/v1/ChristmasGifts', methods=['POST', 'OPTIONS'])
@cross_origin(origin='*')
def create_ChristmasGifts_():
    try:
        query = "insert into ChristmasGifts ('name', 'price','number') values (:name, :price, :number)"
        c1 = conn.cursor()
        c1.execute(query, {
            "name": request.json["name"],
            "price": request.json["price"],
            "number": request.json["number"]}
                   )
        conn.commit()

        return get_ChristmasGifts_by_id(c1.lastrowid)
    except sqlite3.Error as err:
        return to_error_response(' '.join(err.args), "", 500)


@app.route('/api/v1/ChristmasGifts/<int:id>', methods=['PUT'])
def update_ChristmasGifts_by_id(id):
    query = "update ChristmasGifts set 'name' = :name, " \
            "'price' = :price, " \
            "'number' = :number, "




    c1 = conn.cursor()
    c1.execute(query, {
        "name": request.json["name"],
        "price": request.json["price"],
        "number": request.json["number"],
        "id": id
    })
    conn.commit()
    return get_ChristmasGifts_by_id(id)


@app.route('/api/v1/ChristmasGifts/<int:id>', methods=['DELETE'])
@cross_origin()
def delete_ChristmasGifts_by_id(id):
    query = "delete from ChristmasGifts where id= :id"
    c1 = conn.cursor()
    c1.execute(query, {
        "id": id
    })
    conn.commit()
    return to_response(True, "ChristmasGiftsDelete", 200)

if __name__ == '__main__':
    app.run()
