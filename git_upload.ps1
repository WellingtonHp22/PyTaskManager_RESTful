# Script PowerShell para preparar e enviar o projeto ao GitHub
Write-Host "Preparando PyTaskManager_RESTful para envio ao GitHub..." -ForegroundColor Cyan

# Verifica se Git está instalado
try {
    $gitVersion = git --version
    Write-Host "Git detectado: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "Git não encontrado. Por favor, instale o Git e tente novamente." -ForegroundColor Red
    exit
}

# Inicializa o repositório Git (se necessário)
if (-not (Test-Path ".git")) {
    Write-Host "Inicializando repositório Git..." -ForegroundColor Yellow
    git init
}

# Adicionar arquivos essenciais
Write-Host "Adicionando arquivos essenciais..." -ForegroundColor Yellow

# Arquivos principais
git add app.py db.py setup_database.py requirements.txt README.md .gitignore

# Diretórios do projeto
git add models/ resources/ schemas/ static/

# Verificar o status
git status

Write-Host "`nPronto para fazer o commit. Execute os seguintes comandos para enviar ao GitHub:" -ForegroundColor Green
Write-Host "`ngit commit -m `"Versão inicial do PyTaskManager RESTful`"" -ForegroundColor Cyan
Write-Host "git remote add origin https://github.com/WellingtonHp22/PyTaskManager_RESTful.git" -ForegroundColor Cyan
Write-Host "git push -u origin main" -ForegroundColor Cyan

Write-Host "`nSe o repositório já contiver arquivos, você pode precisar executar:" -ForegroundColor Yellow
Write-Host "git pull origin main --allow-unrelated-histories" -ForegroundColor Cyan

Write-Host "`nProjeto preparado com sucesso!" -ForegroundColor Green
