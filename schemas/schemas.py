from marshmallow import Schema, fields, validate, validates, ValidationError
from datetime import datetime

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True, validate=validate.Length(min=3, max=80))
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True, validate=validate.Length(min=6))

class TaskSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    description = fields.Str(validate=validate.Length(max=500))
    status = fields.Str(validate=validate.OneOf(['pendente', 'em_andamento', 'concluida']), default='pendente')
    priority = fields.Str(validate=validate.OneOf(['baixa', 'media', 'alta']), default='media')
    due_date = fields.DateTime(format='%Y-%m-%d %H:%M:%S', allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    user_id = fields.Int(dump_only=True)
    
    @validates('due_date')
    def validate_due_date(self, value):
        if value and value < datetime.utcnow():
            raise ValidationError('A data de vencimento não pode estar no passado.')
