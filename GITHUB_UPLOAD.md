# Instruções para Envio ao GitHub

Este documento contém instruções detalhadas para enviar seu projeto PyTaskManager_RESTful ao GitHub.

## Arquivos Essenciais

Os seguintes arquivos e diretórios são essenciais para o funcionamento da API e devem ser incluídos no repositório:

- **Arquivos Principais**:
  - `app.py`: Ponto de entrada da aplicação
  - `db.py`: Configuração do banco de dados
  - `setup_database.py`: Script para inicialização do banco
  - `requirements.txt`: Dependências do projeto
  - `README.md`: Documentação do projeto
  - `.gitignore`: Configurações para ignorar arquivos desnecessários

- **Diretórios**:
  - `models/`: Definições de modelos de dados
  - `resources/`: Endpoints da API
  - `schemas/`: Validação de dados
  - `static/`: Arquivos estáticos (como documentação Swagger)

## Arquivos a Serem Ignorados

Os seguintes arquivos e diretórios NÃO devem ser incluídos no repositório:

- `__pycache__/` e arquivos `.pyc`: Arquivos de cache Python
- `task_manager.db` e `instance/`: Bancos de dados locais
- `venv/`: Ambiente virtual Python
- `.env`: Contém informações sensíveis como chaves secretas
- `test_api.py`, `test_api_new.py` e `check_port.py`: Arquivos de teste
- `setup.bat`: Script específico para Windows

## Passos para Envio

1. **Usar o Script PowerShell Preparado**

   Execute o script `git_upload.ps1` que irá preparar os arquivos para commit:
   
   ```powershell
   ./git_upload.ps1
   ```

2. **Fazer o Commit**

   ```powershell
   git commit -m "Versão inicial do PyTaskManager RESTful"
   ```

3. **Adicionar o Repositório Remoto**

   ```powershell
   git remote add origin https://github.com/WellingtonHp22/PyTaskManager_RESTful.git
   ```

4. **Enviar para o GitHub**

   ```powershell
   git push -u origin main
   ```

   Se o repositório já tiver sido inicializado com um README no GitHub, pode ser necessário primeiro fazer:
   
   ```powershell
   git pull origin main --allow-unrelated-histories
   ```

## Resolução de Problemas

- **Erro de autenticação**: Certifique-se de estar autenticado no GitHub. Se necessário, configure um token de acesso pessoal.
- **Conflitos de merge**: Se houver conflitos, resolva-os manualmente e faça um novo commit.
- **Arquivos grandes**: Se algum arquivo for muito grande, considere usar Git LFS ou removê-lo.
