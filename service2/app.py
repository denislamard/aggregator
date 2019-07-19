import csv
from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/person/<id>')
def index(id):
    try:
        l = []
        with open('data/Table USERS.csv') as fh:
            reader = csv.DictReader(fh, delimiter=',')
            for row in reader:
                if row['Persons.Per_Id'] == id:
                    l.append(dict(row))
        return jsonify(l), 200
    except Exception as ex:
        return jsonify(str(ex)), 500

if __name__ == '__main__':
    app.run()
