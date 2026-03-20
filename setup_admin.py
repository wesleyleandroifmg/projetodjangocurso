# setup_admin.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projeto_django.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Defina as credenciais iniciais (os alunos podem mudar depois)
username = 'admin'
firstname = 'Admin'
lastname = 'User'
email = 'teste@teste.com'
password = 'SenhaDificil123'

if not User.objects.filter(username=username).exists():
    print(f"Criando superusuário: {username}...")
    User.objects.create_superuser(username, email, password, first_name=firstname, last_name=lastname)
    print("Superusuário criado com sucesso!")
else:
    print("Superusuário já existe.")