# 🚀 PyTaskManager RESTful

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)
![RESTful](https://img.shields.io/badge/API-RESTful-orange.svg)
![JWT](https://img.shields.io/badge/Auth-JWT-yellow.svg)

> **Domine suas tarefas, maximize sua produtividade!** Uma poderosa API RESTful para gerenciamento de tarefas pessoais construída com Flask.

## 📋 Visão Geral

PyTaskManager é uma API RESTful completa para gerenciamento de tarefas pessoais que oferece todas as ferramentas necessárias para organizar seu dia a dia. Com autenticação segura, filtros avançados e análises estatísticas, esta solução foi desenvolvida para tornar o gerenciamento de tarefas uma experiência fluida e eficiente.

![API Demo](https://raw.githubusercontent.com/WellingtonHp22/PyTaskManager_RESTful/main/static/api_demo.png)

## ✨ Funcionalidades

- 🔐 **Autenticação completa** com JWT (JSON Web Tokens)
- 👤 **Gerenciamento de usuários** (registro, login, perfil)
- ✅ **CRUD de tarefas** (criar, listar, atualizar, excluir)
- 🔍 **Filtros avançados** por status, prioridade, data
- 📊 **Estatísticas detalhadas** sobre suas tarefas
- 📁 **Exportação de dados** para formato CSV
- 📝 **Documentação interativa** com Swagger UI

## 🛠️ Tecnologias

- **Python** - Linguagem base do projeto
- **Flask** - Framework web leve e poderoso
- **SQLAlchemy** - ORM para interação com banco de dados
- **Flask-JWT-Extended** - Implementação de autenticação JWT
- **SQLite** - Banco de dados embutido para armazenamento
- **Swagger UI** - Interface interativa para documentação e testes

## 🚦 Como começar

### Pré-requisitos

- Python 3.9 ou superior
- pip (gerenciador de pacotes Python)

### Instalação

1. **Clone este repositório:**
   ```bash
   git clone https://github.com/WellingtonHp22/PyTaskManager_RESTful.git
   cd PyTaskManager_RESTful
   ```

2. **Configure um ambiente virtual (recomendado):**
   ```bash
   python -m venv venv
   
   # No Windows
   venv\Scripts\activate
   
   # No Linux/Mac
   source venv/bin/activate
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure o banco de dados:**
   ```bash
   python setup_database.py
   ```

5. **Execute a aplicação:**
   ```bash
   python app.py
   ```

6. **Acesse a documentação:**
   Abra seu navegador e acesse:
   ```
   http://127.0.0.1:8080/swagger
   ```

## 🔍 Utilizando a API

### Endpoints principais

| Endpoint | Método | Descrição |
|----------|--------|-----------|
| `/register` | POST | Registra um novo usuário no sistema |
| `/login` | POST | Realiza login e retorna token JWT |
| `/logout` | POST | Invalida o token atual (logout) |
| `/tasks` | GET | Lista todas as tarefas do usuário |
| `/tasks` | POST | Cria uma nova tarefa |
| `/task/{id}` | GET | Obtém detalhes de uma tarefa específica |
| `/task/{id}` | PUT | Atualiza uma tarefa existente |
| `/task/{id}` | DELETE | Remove uma tarefa |
| `/tasks/stats` | GET | Obtém estatísticas das tarefas |
| `/tasks/export` | GET | Exporta tarefas para CSV |

### Exemplo de uso (com curl)

1. **Registrar um novo usuário:**
   ```bash
   curl -X POST http://127.0.0.1:8080/register \
     -H "Content-Type: application/json" \
     -d '{"username":"exemplo", "email":"usuario@exemplo.com", "password":"senha123"}'
   ```

2. **Fazer login:**
   ```bash
   curl -X POST http://127.0.0.1:8080/login \
     -H "Content-Type: application/json" \
     -d '{"username":"exemplo", "password":"senha123"}'
   ```

3. **Obter suas tarefas (com token):**
   ```bash
   curl -X GET http://127.0.0.1:8080/tasks \
     -H "Authorization: Bearer SEU_TOKEN_JWT"
   ```

## 📈 Próximas melhorias planejadas

- [ ] Notificações por e-mail para tarefas próximas do prazo
- [ ] Suporte a mais formatos de exportação (JSON, XML, Excel)
- [ ] Interface web para consumir a API
- [ ] Integração com calendários externos
- [ ] Tarefas recorrentes e compartilháveis
- [ ] Aplicativo mobile

## 📄 Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 👤 Autor

**Wellington Santos**

- GitHub: [@WellingtonHp22](https://github.com/WellingtonHp22)

---

⭐️ Se este projeto foi útil para você, considere deixar uma estrela! ⭐️
- `POST /logout` - Logout de usuário (requer JWT)

### Usuários
- `POST /register` - Registro de novo usuário
- `POST /login` - Login de usuário
- `POST /logout` - Logout de usuário (requer JWT)
- `GET /user/me` - Obtém informações do usuário atual (requer JWT)

### Tarefas
- `GET /tasks` - Lista todas as tarefas do usuário com suporte à paginação (requer JWT)
- `POST /tasks` - Cria uma nova tarefa (requer JWT)
- `GET /task/{id}` - Obtém detalhes de uma tarefa específica (requer JWT)
- `PUT /task/{id}` - Atualiza uma tarefa existente (requer JWT)
- `DELETE /task/{id}` - Exclui uma tarefa (requer JWT)

### Estatísticas e Exportação
- `GET /tasks/stats` - Obtém estatísticas sobre as tarefas do usuário (requer JWT)
- `GET /tasks/export` - Exporta as tarefas do usuário para CSV (requer JWT)

## Exemplos de Uso

### Registro de usuário
```
POST /register
Content-Type: application/json

{
  "username": "usuario",
  "email": "usuario@example.com",
  "password": "senha123"
}
```

### Login
```
POST /login
Content-Type: application/json

{
  "username": "usuario",
  "password": "senha123"
}
```

### Criação de tarefa
```
POST /tasks
Authorization: Bearer {seu-token-jwt}
Content-Type: application/json

{
  "title": "Implementar API Flask",
  "description": "Desenvolver uma API RESTful utilizando Flask",
  "status": "pendente",
  "priority": "alta",
  "due_date": "2025-05-20 23:59:59"
}
```

### Listagem de tarefas com paginação e ordenação
```
GET /tasks?page=2&per_page=10&sort_by=due_date&sort_order=asc&status=pendente
Authorization: Bearer {seu-token-jwt}
```

### Obtenção de estatísticas
```
GET /tasks/stats
Authorization: Bearer {seu-token-jwt}
```

### Exportação para CSV
```
GET /tasks/export
Authorization: Bearer {seu-token-jwt}
```

## Contribuição

Sinta-se à vontade para contribuir com este projeto. Faça um fork, implemente suas alterações e envie um pull request.
