import csv
from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/phone/<personid>')
def index(personid):
    try:
        l = []
        with open('data/Table MOBILE_LINES.csv') as fh:
            reader = csv.DictReader(fh, delimiter=',')
            for row in reader:
                if row['mobile.user_person_id'] == personid:
                    l.append(dict(row))
        return jsonify(l), 200
    except Exception as ex:
        return jsonify(str(ex)), 500

if __name__ == '__main__':
    app.run()
