import os
import sys

# Adiciona o diretório raiz do projeto ao caminho de importação
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, send_from_directory
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# Inicializa a aplicação Flask
app = Flask(__name__)
CORS(app)

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['JWT_ERROR_MESSAGE_KEY'] = 'message'
app.config['PROPAGATE_EXCEPTIONS'] = True

# Inicializa JWT
jwt = JWTManager(app)

# Importação da lista negra de tokens
from resources.user import blacklist

# Verifica se o token está na lista negra
@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, jwt_payload):
    jti = jwt_payload['jti']
    return jti in blacklist

# Mensagem quando o token está na lista negra
@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return {
        'message': 'O token foi invalidado',
        'error': 'token_revoked'
    }, 401

# Inicializa a API
api = Api(app)

# Configuração do Swagger UI
SWAGGER_URL = '/api/docs'  # URL para acessar a UI do Swagger
API_URL = '/static/swagger.json'  # Onde a especificação Swagger está hospedada

# Configuração do blueprint do Swagger UI
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "API RESTful de Gerenciamento de Tarefas"
    }
)

# Registro do blueprint
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# Endpoint para a rota raiz (redirecionamento para a documentação)
@app.route('/')
def index():
    from flask import redirect
    return redirect('/api/docs')

# Endpoint para servir o arquivo swagger.json
@app.route('/static/swagger.json')
def serve_swagger_spec():
    return send_from_directory('static', 'swagger.json')

# Importações dos recursos
from resources.user import UserRegister, UserLogin, UserLogout, UserInfo
from resources.task import Task, TaskList
from resources.stats import TaskStats
from resources.export import TaskExport

# Rotas da API
api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(UserInfo, '/user/me')
api.add_resource(Task, '/task/<int:task_id>')
api.add_resource(TaskList, '/tasks')
api.add_resource(TaskStats, '/tasks/stats')
api.add_resource(TaskExport, '/tasks/export')

# Importa e inicializa o banco de dados
from db import db
db.init_app(app)

# Cria um contexto de aplicação para criar as tabelas
with app.app_context():
    db.create_all()

# Executa o aplicativo
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
