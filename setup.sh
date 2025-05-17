#!/bin/bash

# Nome do ambiente virtual
VENV_NAME="codelab_venv"

echo "Criando ambiente virtual ($VENV_NAME)..."
python3 -m venv $VENV_NAME

echo "Ambiente virtual criado com sucesso."

echo "Ativando o ambiente virtual..."
source $VENV_NAME/bin/activate

echo "Ambiente virtual ativado."

echo "Instalando dependências..."
pip install -r requirements.txt

echo "Dependências instaladas com sucesso."

echo "Pronto! Use 'source $VENV_NAME/bin/activate' para ativar o ambiente virtual."
source $VENV_NAME/bin/activate