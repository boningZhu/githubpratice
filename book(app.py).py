import json
import sqlite3

from flask import Flask, jsonify, request, Response
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

conn = sqlite3.connect(r"books.db", check_same_thread=False)
c = conn.cursor()
c.execute(
    """
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        bookName text,
        priceNumber text,
        ISBN text,
        type text
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


@app.route('/api/v1/books', methods=['GET'])
def get_book_list():
    c1 = conn.cursor()
    query = "select * from books"
    c1.execute(query)
    results = c1.fetchall()
    book_list = []
    for result in results:
        book_list.append({
            "id": result[0],
            "bookName": result[1],
            "priceNumber": result[2],
            "ISBN": result[3],
            "type": result[4]
        })
    return to_response(book_list, "book list loaded", 200)


@app.route('/api/v1/books/<int:id>', methods=['GET'])
def get_book_by_id(id):
    try:
        c1 = conn.cursor()
        query = "select * from books where id = :id"
        c1.execute(query, {"id": id})
        result = c1.fetchone()
        founded_book = {
            "id": result[0],
            "bookName": result[1],
            "priceNumber": result[2],
            "ISBN": result[3],
            "type": result[4]
        }
        return to_response(founded_book, "book loaded", 200)
    except sqlite3.Error as err:
        return to_error_response(' '.join(err.args), "", 500)


@app.route('/api/v1/books', methods=['POST'])
def create_book():
    try:
        query = "insert into books ('bookName', 'priceNumber','ISBN','type') values (:bookName, :priceNumber, :ISBN, :type)"
        c1 = conn.cursor()
        c1.execute(query, {
            "bookName": request.json["bookName"],
            "priceNumber": request.json["priceNumber"],
            "ISBN": request.json["ISBN"],
            "type": request.json["type"]}
                   )
        conn.commit()

        return get_book_by_id(c1.lastrowid)
    except sqlite3.Error as err:
        return to_error_response(' '.join(err.args), "", 500)


@app.route('/api/v1/books/<int:id>', methods=['PUT'])
def update_book_by_id(id):
    query = "update books set 'bookName' = :bookName, " \
            "'priceNumber' = :priceNumber, " \
            "'ISBN' = :ISBN, " \
            "'type' = :type where id= :id"

    c1 = conn.cursor()
    c1.execute(query, {
        "bookName": request.json["bookName"],
        "priceNumber": request.json["priceNumber"],
        "ISBN": request.json["ISBN"],
        "type": request.json["type"],
        "id": id
    })
    conn.commit()
    return get_book_by_id(id)


@app.route('/api/v1/books/<int:id>', methods=['DELETE'])
def delete_book_by_id(id):
    query = "delete from books where id= :id"
    c1 = conn.cursor()
    c1.execute(query, {
        "id": id
    })
    conn.commit()
    return to_response(True, "bookDelete", 200)


if __name__ == '__main__':
    app.run()
