#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script principal para iniciar a Plataforma Inteligente da Clearview Capital.
Este script inicializa todos os componentes do sistema e inicia o servidor.
"""

import os
import sys
import logging
import threading
import time
from datetime import datetime

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("clearview_platform.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("ClearviewPlatform")

# Adicionar diretórios ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend"))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend/analysis"))

# Importar módulos do sistema
try:
    from backend.api_server import app
    from backend.analysis.stock_analyzer import StockAnalyzer
    from backend.analysis.ai_integration import AIIntegration
    from backend.notification_system import NotificationSystem
    
    logger.info("Módulos importados com sucesso")
except ImportError as e:
    logger.error(f"Erro ao importar módulos: {e}")
    sys.exit(1)

def run_scheduled_tasks(notification_system, analyzer):
    """
    Executa tarefas agendadas em segundo plano.
    
    Args:
        notification_system (NotificationSystem): Sistema de notificações
        analyzer (StockAnalyzer): Analisador de ações
    """
    logger.info("Iniciando thread de tarefas agendadas")
    
    while True:
        try:
            # Executar tarefas agendadas
            results = notification_system.run_scheduled_tasks()
            
            # Atualizar carteira a cada 24 horas
            now = datetime.now()
            if now.hour == 18 and now.minute == 0:  # 18:00
                logger.info("Atualizando carteira")
                portfolio = analyzer.update_portfolio()
                logger.info(f"Carteira atualizada com {len(portfolio.get('stocks', []))} ações")
            
            # Verificar oportunidades a cada hora
            if now.minute == 0:  # A cada hora
                logger.info("Verificando oportunidades")
                favorites = analyzer.get_favorites()
                
                # Notificar sobre oportunidades
                for stock in favorites:
                    notification_system.notify_opportunity(stock)
            
            # Aguardar 1 minuto antes da próxima verificação
            time.sleep(60)
        except Exception as e:
            logger.error(f"Erro na execução de tarefas agendadas: {e}")
            time.sleep(60)  # Aguardar 1 minuto antes de tentar novamente

def main():
    """Função principal para iniciar a plataforma."""
    logger.info("Iniciando Plataforma Inteligente da Clearview Capital")
    
    # Diretório de dados
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
    os.makedirs(data_dir, exist_ok=True)
    
    # Inicializar componentes
    try:
        # Analisador de ações
        analyzer = StockAnalyzer(data_dir=data_dir)
        logger.info("Analisador de ações inicializado")
        
        # Integração com IA
        ai = AIIntegration(data_dir=data_dir)
        logger.info("Integração com IA inicializada")
        
        # Sistema de notificações
        notification_system = NotificationSystem(data_dir=data_dir)
        logger.info("Sistema de notificações inicializado")
        
        # Inicializar dados
        logger.info("Inicializando dados...")
        portfolio = analyzer.update_portfolio()
        logger.info(f"Carteira inicializada com {len(portfolio.get('stocks', []))} ações")
        
        # Iniciar thread para tarefas agendadas
        scheduler_thread = threading.Thread(
            target=run_scheduled_tasks,
            args=(notification_system, analyzer),
            daemon=True
        )
        scheduler_thread.start()
        logger.info("Thread de tarefas agendadas iniciada")
        
        # Iniciar servidor API
        logger.info("Iniciando servidor API na porta 5000...")
        app.run(host='0.0.0.0', port=5000, debug=False)
    except Exception as e:
        logger.error(f"Erro ao iniciar plataforma: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
