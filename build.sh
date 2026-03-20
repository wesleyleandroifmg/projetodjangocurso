#!/usr/bin/env bash
# Sair se houver erro
set -o errexit # Diz ao script para parar imediatamente se qualquer comando falhar. Isso evita que o site suba com erro.

pip install -r requirements.txt # Instala o Django e todas as bibliotecas necessárias no servidor do Render.
# Pega todos os arquivos CSS, JS e imagens do seu projeto e os organiza em uma pasta única para que o WhiteNoise consiga servi-los.
python manage.py collectstatic --no-input
# Atualiza o banco de dados PostgreSQL do Render com as tabelas do seu projeto automaticamente.
python manage.py migrate