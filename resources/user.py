from flask_restful import Resource
from flask import request
# Usando importações relativas para tornar o código mais robusto
# em relação ao local de execução
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.user import UserModel
from schemas.schemas import UserSchema
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
import datetime

user_schema = UserSchema()

# Lista negra de tokens para logout
blacklist = set()

class UserRegister(Resource):
    def post(self):
        # Valida e deserializa os dados de entrada
        try:
            user_data = user_schema.load(request.get_json())
        except Exception as e:
            return {"message": "Erro de validação", "errors": str(e)}, 400
            
        # Verifica se o usuário já existe
        if UserModel.find_by_username(user_data['username']):
            return {"message": "Um usuário com este nome já existe"}, 400
            
        if UserModel.find_by_email(user_data['email']):
            return {"message": "Um usuário com este e-mail já existe"}, 400
            
        # Cria um novo usuário
        user = UserModel(
            username=user_data['username'],
            email=user_data['email']
        )
        user.password = user_data['password']
        
        try:
            user.save_to_db()
            return {"message": "Usuário criado com sucesso"}, 201
        except Exception as e:
            return {"message": "Erro ao criar usuário", "error": str(e)}, 500


class UserLogin(Resource):
    def post(self):
        try:
            data = request.get_json()
            
            # Tenta autenticar por nome de usuário ou email
            user = UserModel.find_by_username(data['username'])
            if not user:
                user = UserModel.find_by_email(data['username'])
                
            if user and user.verify_password(data['password']):
                # Cria token de acesso com expiração de 1 hora
                access_token = create_access_token(
                    identity=user.id,
                    fresh=True,
                    expires_delta=datetime.timedelta(hours=1)
                )
                
                return {
                    'message': 'Login realizado com sucesso',
                    'access_token': access_token,
                    'user_id': user.id,
                    'username': user.username
                }, 200
            return {"message": "Credenciais inválidas"}, 401
            
        except Exception as e:
            return {"message": "Erro ao fazer login", "error": str(e)}, 500


class UserLogout(Resource):
    @jwt_required()
    def post(self):
        jti = get_jwt()['jti']
        blacklist.add(jti)
        return {"message": "Logout realizado com sucesso"}, 200


class UserInfo(Resource):
    @jwt_required()
    def get(self):
        # Obtém o ID do usuário autenticado
        user_id = get_jwt_identity()
        
        # Busca o usuário pelo ID
        user = UserModel.find_by_id(user_id)
        
        if not user:
            return {'message': 'Usuário não encontrado'}, 404
            
        # Retorna os dados do usuário
        return user.json(), 200
