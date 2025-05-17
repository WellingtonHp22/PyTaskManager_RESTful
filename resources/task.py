from flask_restful import Resource
from flask import request
# Usando importações relativas para tornar o código mais robusto
# em relação ao local de execução
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.task import TaskModel
from schemas.schemas import TaskSchema
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from sqlalchemy import case

task_schema = TaskSchema()

class Task(Resource):
    @jwt_required()
    def get(self, task_id):
        # Obtém o ID do usuário autenticado
        user_id = get_jwt_identity()
        
        # Busca a tarefa pelo ID
        task = TaskModel.find_by_id(task_id)
        
        # Verifica se a tarefa existe
        if not task:
            return {'message': 'Tarefa não encontrada'}, 404
            
        # Verifica se a tarefa pertence ao usuário
        if task.user_id != user_id:
            return {'message': 'Acesso negado'}, 403
            
        return task.json(), 200
        
    @jwt_required()
    def put(self, task_id):
        # Obtém o ID do usuário autenticado
        user_id = get_jwt_identity()
        
        # Busca a tarefa pelo ID
        task = TaskModel.find_by_id(task_id)
        
        # Verifica se a tarefa existe
        if not task:
            return {'message': 'Tarefa não encontrada'}, 404
            
        # Verifica se a tarefa pertence ao usuário
        if task.user_id != user_id:
            return {'message': 'Acesso negado'}, 403
            
        # Valida os dados de entrada
        try:
            data = task_schema.load(request.get_json(), partial=True)
        except Exception as e:
            return {'message': 'Erro na validação dos dados', 'errors': str(e)}, 400
            
        # Atualiza os campos da tarefa
        if 'title' in data:
            task.title = data['title']
        if 'description' in data:
            task.description = data['description']
        if 'status' in data:
            task.status = data['status']
        if 'priority' in data:
            task.priority = data['priority']
        if 'due_date' in data:
            task.due_date = data['due_date']
            
        # Salva no banco de dados
        task.save_to_db()
        
        return {'message': 'Tarefa atualizada com sucesso', 'task': task.json()}, 200
        
    @jwt_required()
    def delete(self, task_id):
        # Obtém o ID do usuário autenticado
        user_id = get_jwt_identity()
        
        # Busca a tarefa pelo ID
        task = TaskModel.find_by_id(task_id)
        
        # Verifica se a tarefa existe
        if not task:
            return {'message': 'Tarefa não encontrada'}, 404
            
        # Verifica se a tarefa pertence ao usuário
        if task.user_id != user_id:
            return {'message': 'Acesso negado'}, 403
            
        # Deleta a tarefa do banco de dados
        task.delete_from_db()
        
        return {'message': 'Tarefa excluída com sucesso'}, 200


class TaskList(Resource):
    @jwt_required()
    def get(self):
        # Obtém o ID do usuário autenticado
        user_id = get_jwt_identity()
        
        # Parâmetros de filtro
        status = request.args.get('status')
        priority = request.args.get('priority')
        sort_by = request.args.get('sort_by', 'due_date')  # Ordenação (due_date, created_at, priority)
        sort_order = request.args.get('sort_order', 'asc')  # Ordem (asc, desc)
        
        # Parâmetros de paginação
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        
        # Verifica limites para per_page
        if per_page > 50:
            per_page = 50  # Limita o máximo de itens por página
        
        # Busca todas as tarefas do usuário
        tasks_query = TaskModel.find_all_by_user(user_id)
        
        # Aplica filtros se necessário
        if status:
            tasks_query = tasks_query.filter(TaskModel.status == status)
        if priority:
            tasks_query = tasks_query.filter(TaskModel.priority == priority)
        
        # Aplica ordenação
        if sort_by == 'created_at':
            if sort_order == 'desc':
                tasks_query = tasks_query.order_by(TaskModel.created_at.desc())
            else:
                tasks_query = tasks_query.order_by(TaskModel.created_at.asc())
        elif sort_by == 'priority':
            # Ordenação manual por prioridade após a consulta
            # A ordenação será feita na memória depois de obter os resultados
            if sort_order == 'desc':
                tasks_query = tasks_query.order_by(TaskModel.created_at.desc())  # Ordenação secundária
            else:
                tasks_query = tasks_query.order_by(TaskModel.created_at.asc())  # Ordenação secundária
        else:  # due_date (padrão)
            if sort_order == 'desc':
                tasks_query = tasks_query.order_by(TaskModel.due_date.desc())
            else:
                tasks_query = tasks_query.order_by(TaskModel.due_date.asc())
        
        # Executa a paginação
        total_tasks = tasks_query.count()
        total_pages = (total_tasks + per_page - 1) // per_page  # Cálculo de páginas necessárias
        
        # Ajusta a página se estiver fora dos limites
        if page < 1:
            page = 1
        if page > total_pages and total_pages > 0:
            page = total_pages
            
        # Obtém os itens da página atual
        tasks = tasks_query.offset((page - 1) * per_page).limit(per_page).all()
        
        # Prepara resposta com metadados de paginação
        response = {
            'tasks': [task.json() for task in tasks],
            'pagination': {
                'total_tasks': total_tasks,
                'per_page': per_page,
                'current_page': page,
                'total_pages': total_pages,
                'has_next': page < total_pages,
                'has_prev': page > 1
            }
        }
        
        return response, 200
        
    @jwt_required()
    def post(self):
        # Obtém o ID do usuário autenticado
        user_id = get_jwt_identity()
        
        # Valida e deserializa os dados de entrada
        try:
            data = task_schema.load(request.get_json())
        except Exception as e:
            return {'message': 'Erro na validação dos dados', 'errors': str(e)}, 400
        
        # Formato a data se ela existir
        due_date = None
        if 'due_date' in data and data['due_date']:
            due_date = data['due_date']
            
        # Cria uma nova tarefa
        task = TaskModel(
            title=data['title'],
            description=data.get('description', ''),
            status=data.get('status', 'pendente'),
            priority=data.get('priority', 'media'),
            due_date=due_date,
            user_id=user_id
        )
        
        try:
            # Salva no banco de dados
            task.save_to_db()
            return {'message': 'Tarefa criada com sucesso', 'task': task.json()}, 201
        except Exception as e:
            return {'message': 'Erro ao criar tarefa', 'error': str(e)}, 500
