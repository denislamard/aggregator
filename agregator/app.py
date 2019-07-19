import json
import requests
import business
from flask import Flask, escape, request, jsonify, abort

app = Flask(__name__)
business = business.Agregator()

types = {
    "integer": lambda v: str.isdigit(v),
    "string": lambda v: isinstance(str(v), str)
}


@app.route('/', methods=['GET'])
def root_page():
    return 'Hello, World!'


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'GET':
        return jsonify(business.routes), 200
    else:
        if not request.json:
            abort(400)
        business.addentry(request.json)
        return json.dumps(request.json), 201


@app.route('/<path:subpath>', methods=['GET', 'POST'])
def index(subpath):
    if request.method == 'POST':
        pass
    else:
        route = business.findentry(escape(subpath))
        if route is None:
            return jsonify(error=404, text='{} is not available'.format(escape(subpath))), 404
        # get parameters for querystring
        parametersvalues = {}
        for p in route['parameters']:
            value = request.args.get(p['name'])
            if value is not None:
                if types[p['type']](value):
                    parametersvalues[p['name']] = value
                else:
                    return jsonify(error=400,
                                   text='the value {} of the parameter {} is not a valid {}'.format(value, p['name'],
                                                                                                    p['type'])), 400
            else:
                return jsonify(error=400, text='parameter {} is mandatory'.format(p['name'])), 400

        # call all services
        response = {}
        for service in route['services']:
            data = requests.get(service['url'].format(**parametersvalues))
            if data.status_code != 200:
                return jsonify('failed to get data'), data.status_code
            if service['type'] == 'object':
                if len(data.json()) == 0:
                    return jsonify('no data to load'), 404
                response['object'] = data.json()[0]
            else:
                response['collection'] = {}
                response['collection']['version'] = '1.0.0'
                response['collection']['items'] = data.json()
        return jsonify(response), 200


if __name__ == '__main__':
    app.run(port=8080)
