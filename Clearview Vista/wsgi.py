#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Arquivo WSGI para implantação da Plataforma Inteligente da Clearview Capital.
Este arquivo é usado pelo Gunicorn para servir a aplicação em ambiente de produção.
"""

import os
import sys

# Adicionar diretórios ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend"))

# Importar a aplicação Flask
from backend.api_server import app

# Para execução com Gunicorn
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
