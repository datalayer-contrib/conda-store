import datetime

from flask import jsonify, Flask, g, request, Response

from conda_store.data_model.base import DatabaseManager
from conda_store.data_model import api


def start_ui_server(conda_store, address='0.0.0.0', port=5000):
    app = Flask(__name__)

    def get_dbm(conda_store):
        dbm = getattr(g, '_dbm', None)
        if dbm is None:
            dbm = g._dbm = DatabaseManager(conda_store)
        return dbm

    @app.teardown_appcontext
    def close_connection(exception):
        dbm = getattr(g, '_dbm', None)
        if dbm is not None:
            dbm.close()

    @app.route('/')
    def index():
        return "This is the environment page"

    @app.route('/api/v1/')
    def api_status():
        return jsonify({"status": "ok"})

    @app.route('/api/v1/environment/')
    def list_environments():
        dbm = get_dbm(conda_store)
        return jsonify(api.list_environments(dbm))

    @app.route('/api/v1/specification/', methods=['GET'])
    def list_specification():
        dbm = get_dbm(conda_store)
        return jsonify(api.list_specifications(dbm))

    @app.route('/api/v1/specification/', methods=['POST'])
    def post_specification():
        dbm = get_dbm(conda_store)
        return jsonify(api.post_specifications(dbm, request.json))

    @app.route('/api/v1/specification/<spec>/', methods=['GET'])
    def get_specification(spec):
        dbm = get_dbm(conda_store)
        return jsonify(api.get_specification(dbm, spec))

    @app.route('/api/v1/build/<build>/', methods=['GET'])
    def get_build(build):
        dbm = get_dbm(conda_store)
        return jsonify(api.get_build(dbm, build))

    @app.route('/api/v1/build/<build>/logs/', methods=['GET'])
    def get_build_logs(build):
        dbm = get_dbm(conda_store)
        return Response(
            api.get_build_logs(dbm, build),
            mimetype='text/plain')

    @app.route('/api/v1/environment/<name>/', methods=['DELETE'])
    def delete_environment(name):
        return jsonify({'name': name, 'last_modified': datetime.datetime.now()})

    app.run(debug=True, host=address, port=port)