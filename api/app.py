from flask import Flask
from flask_cors import CORS

from controllers.buscar_controller import operadora_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(operadora_bp)

port = 5000
host = 'localhost'

app.run(port=port, host=host, debug=True)