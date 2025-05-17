from flask_restful import Resource
from flask import request
# Usando importações relativas para tornar o código mais robusto
# em relação ao local de execução
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.task import TaskModel
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import func
from db import db

class TaskStats(Resource):
    @jwt_required()
    def get(self):
        # Obtém o ID do usuário autenticado
        user_id = get_jwt_identity()
        
        # Estatísticas por status
        status_stats = db.session.query(
            TaskModel.status,
            func.count(TaskModel.id)
        ).filter(
            TaskModel.user_id == user_id
        ).group_by(
            TaskModel.status
        ).all()
        
        # Estatísticas por prioridade
        priority_stats = db.session.query(
            TaskModel.priority,
            func.count(TaskModel.id)
        ).filter(
            TaskModel.user_id == user_id
        ).group_by(
            TaskModel.priority
        ).all()
        
        # Contagem total de tarefas
        total_tasks = TaskModel.query.filter_by(user_id=user_id).count()
        
        # Tarefas vencidas (com data limite no passado e não concluídas)
        from datetime import datetime
        overdue_tasks = TaskModel.query.filter(
            TaskModel.user_id == user_id,
            TaskModel.due_date < datetime.utcnow(),
            TaskModel.status != 'concluida'
        ).count()
        
        # Formata os resultados
        result = {
            'total_tasks': total_tasks,
            'overdue_tasks': overdue_tasks,
            'status': {s[0]: s[1] for s in status_stats},
            'priority': {p[0]: p[1] for p in priority_stats}
        }
        
        return result, 200
