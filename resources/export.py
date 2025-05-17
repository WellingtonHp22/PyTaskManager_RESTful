from flask_restful import Resource
from flask import make_response
# Usando importações relativas para tornar o código mais robusto
# em relação ao local de execução
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.task import TaskModel
from flask_jwt_extended import jwt_required, get_jwt_identity
import csv
import io
import datetime

class TaskExport(Resource):
    @jwt_required()
    def get(self):
        # Obtém o ID do usuário autenticado
        user_id = get_jwt_identity()
        
        # Busca todas as tarefas do usuário
        tasks = TaskModel.query.filter_by(user_id=user_id).all()
        
        # Prepara o buffer para o CSV
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Escreve o cabeçalho
        writer.writerow(['ID', 'Título', 'Descrição', 'Status', 'Prioridade', 
                        'Data de Vencimento', 'Criada em', 'Atualizada em'])
        
        # Escreve as linhas de dados
        for task in tasks:
            writer.writerow([
                task.id,
                task.title,
                task.description,
                task.status,
                task.priority,
                task.due_date.strftime('%Y-%m-%d %H:%M:%S') if task.due_date else '',
                task.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                task.updated_at.strftime('%Y-%m-%d %H:%M:%S')
            ])
        
        # Preparar a resposta
        output.seek(0)
        
        # Gera um nome de arquivo com a data atual
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        filename = f"tarefas_{today}.csv"
        
        # Cria a resposta com o conteúdo do CSV
        response = make_response(output.getvalue())
        response.headers['Content-Disposition'] = f'attachment; filename="{filename}"'
        response.headers['Content-type'] = 'text/csv; charset=utf-8'
        
        return response
