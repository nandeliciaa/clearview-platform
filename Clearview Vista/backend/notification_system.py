#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Sistema de notificações para a Plataforma Inteligente da Clearview Capital.
Este módulo implementa o envio de notificações por diferentes canais:
- E-mail
- Telegram
- Notificações push no navegador
- Alertas na plataforma
"""

import os
import sys
import json
import logging
from datetime import datetime
import time
import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Adicionar diretório pai ao path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from analysis.ai_integration import AIIntegration

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("notification_system.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("NotificationSystem")

class NotificationSystem:
    """
    Classe para gerenciamento e envio de notificações por diferentes canais.
    """
    
    def __init__(self, data_dir="/home/ubuntu/clearview_project/data"):
        """
        Inicializa o sistema de notificações.
        
        Args:
            data_dir (str): Diretório para armazenamento de dados
        """
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
        
        # Inicializar integração com IA para geração de conteúdo
        self.ai = AIIntegration(data_dir=data_dir)
        
        # Carregar configurações
        self.config = self.load_config()
        
        # Carregar assinantes da newsletter
        self.subscribers = self.load_subscribers()
        
        # Carregar alertas configurados
        self.alerts = self.load_alerts()
        
        # Histórico de notificações enviadas
        self.notification_history = self.load_notification_history()
    
    def load_config(self):
        """Carrega configurações do sistema de notificações."""
        try:
            config_file = os.path.join(self.data_dir, "notification_config.json")
            if os.path.exists(config_file):
                with open(config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            
            # Configuração padrão
            default_config = {
                "email": {
                    "enabled": True,
                    "smtp_server": "smtp.gmail.com",
                    "smtp_port": 587,
                    "smtp_user": "clearview.capital@gmail.com",
                    "smtp_password": "",  # Em produção, usar variáveis de ambiente
                    "from_name": "Clearview Capital"
                },
                "telegram": {
                    "enabled": True,
                    "bot_token": "",  # Em produção, usar variáveis de ambiente
                    "channel_id": "@Clearview_Capital_Bot"
                },
                "push": {
                    "enabled": True,
                    "vapid_public_key": "",  # Em produção, usar variáveis de ambiente
                    "vapid_private_key": ""  # Em produção, usar variáveis de ambiente
                },
                "platform": {
                    "enabled": True
                },
                "schedule": {
                    "daily_newsletter": "18:00",  # Horário para envio da newsletter diária
                    "market_open_alert": "10:00",  # Horário para alerta de abertura do mercado
                    "market_close_alert": "17:30",  # Horário para alerta de fechamento do mercado
                    "opportunity_check": "12:00,15:00"  # Horários para verificação de oportunidades
                }
            }
            
            # Salvar configuração padrão
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, ensure_ascii=False, indent=2)
            
            return default_config
        except Exception as e:
            logger.error(f"Erro ao carregar configurações: {e}")
            return {}
    
    def save_config(self):
        """Salva configurações do sistema de notificações."""
        try:
            config_file = os.path.join(self.data_dir, "notification_config.json")
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
            logger.info(f"Configurações salvas em {config_file}")
        except Exception as e:
            logger.error(f"Erro ao salvar configurações: {e}")
    
    def load_subscribers(self):
        """Carrega lista de assinantes da newsletter."""
        try:
            subscribers_file = os.path.join(self.data_dir, "newsletter_subscribers.json")
            if os.path.exists(subscribers_file):
                with open(subscribers_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return []
        except Exception as e:
            logger.error(f"Erro ao carregar assinantes: {e}")
            return []
    
    def save_subscribers(self):
        """Salva lista de assinantes da newsletter."""
        try:
            subscribers_file = os.path.join(self.data_dir, "newsletter_subscribers.json")
            with open(subscribers_file, 'w', encoding='utf-8') as f:
                json.dump(self.subscribers, f, ensure_ascii=False, indent=2)
            logger.info(f"Assinantes salvos em {subscribers_file}")
        except Exception as e:
            logger.error(f"Erro ao salvar assinantes: {e}")
    
    def load_alerts(self):
        """Carrega alertas configurados."""
        try:
            alerts_file = os.path.join(self.data_dir, "alerts.json")
            if os.path.exists(alerts_file):
                with open(alerts_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return []
        except Exception as e:
            logger.error(f"Erro ao carregar alertas: {e}")
            return []
    
    def save_alerts(self):
        """Salva alertas configurados."""
        try:
            alerts_file = os.path.join(self.data_dir, "alerts.json")
            with open(alerts_file, 'w', encoding='utf-8') as f:
                json.dump(self.alerts, f, ensure_ascii=False, indent=2)
            logger.info(f"Alertas salvos em {alerts_file}")
        except Exception as e:
            logger.error(f"Erro ao salvar alertas: {e}")
    
    def load_notification_history(self):
        """Carrega histórico de notificações enviadas."""
        try:
            history_file = os.path.join(self.data_dir, "notification_history.json")
            if os.path.exists(history_file):
                with open(history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return []
        except Exception as e:
            logger.error(f"Erro ao carregar histórico de notificações: {e}")
            return []
    
    def save_notification_history(self):
        """Salva histórico de notificações enviadas."""
        try:
            history_file = os.path.join(self.data_dir, "notification_history.json")
            with open(history_file, 'w', encoding='utf-8') as f:
                json.dump(self.notification_history, f, ensure_ascii=False, indent=2)
            logger.info(f"Histórico de notificações salvo em {history_file}")
        except Exception as e:
            logger.error(f"Erro ao salvar histórico de notificações: {e}")
    
    def add_subscriber(self, email, name="", phone=""):
        """
        Adiciona um novo assinante à newsletter.
        
        Args:
            email (str): E-mail do assinante
            name (str): Nome do assinante
            phone (str): Telefone do assinante
            
        Returns:
            bool: True se adicionado com sucesso, False caso contrário
        """
        logger.info(f"Adicionando assinante: {email}")
        
        # Verificar se o e-mail já está cadastrado
        for subscriber in self.subscribers:
            if subscriber.get('email') == email:
                logger.warning(f"E-mail já cadastrado: {email}")
                return False
        
        # Adicionar novo assinante
        self.subscribers.append({
            'email': email,
            'name': name,
            'phone': phone,
            'date': datetime.now().isoformat(),
            'active': True
        })
        
        # Salvar lista atualizada
        self.save_subscribers()
        
        # Enviar e-mail de boas-vindas
        self.send_welcome_email(email, name)
        
        return True
    
    def remove_subscriber(self, email):
        """
        Remove um assinante da newsletter.
        
        Args:
            email (str): E-mail do assinante
            
        Returns:
            bool: True se removido com sucesso, False caso contrário
        """
        logger.info(f"Removendo assinante: {email}")
        
        # Procurar assinante
        for i, subscriber in enumerate(self.subscribers):
            if subscriber.get('email') == email:
                # Marcar como inativo em vez de remover
                self.subscribers[i]['active'] = False
                self.subscribers[i]['unsubscribe_date'] = datetime.now().isoformat()
                
                # Salvar lista atualizada
                self.save_subscribers()
                
                # Enviar e-mail de confirmação
                self.send_unsubscribe_confirmation(email, subscriber.get('name', ''))
                
                return True
        
        logger.warning(f"Assinante não encontrado: {email}")
        return False
    
    def create_alert(self, user_id, alert_type, params):
        """
        Cria um novo alerta.
        
        Args:
            user_id (str): ID do usuário
            alert_type (str): Tipo de alerta (price, target, opportunity, news)
            params (dict): Parâmetros do alerta
            
        Returns:
            str: ID do alerta criado
        """
        logger.info(f"Criando alerta para usuário {user_id}: {alert_type}")
        
        # Gerar ID único para o alerta
        alert_id = f"alert_{int(time.time())}_{user_id}"
        
        # Criar alerta
        alert = {
            'id': alert_id,
            'user_id': user_id,
            'type': alert_type,
            'params': params,
            'created_at': datetime.now().isoformat(),
            'active': True,
            'last_triggered': None
        }
        
        # Adicionar à lista de alertas
        self.alerts.append(alert)
        
        # Salvar lista atualizada
        self.save_alerts()
        
        return alert_id
    
    def update_alert(self, alert_id, params=None, active=None):
        """
        Atualiza um alerta existente.
        
        Args:
            alert_id (str): ID do alerta
            params (dict): Novos parâmetros do alerta
            active (bool): Novo estado do alerta
            
        Returns:
            bool: True se atualizado com sucesso, False caso contrário
        """
        logger.info(f"Atualizando alerta: {alert_id}")
        
        # Procurar alerta
        for i, alert in enumerate(self.alerts):
            if alert.get('id') == alert_id:
                # Atualizar parâmetros, se fornecidos
                if params is not None:
                    self.alerts[i]['params'] = params
                
                # Atualizar estado, se fornecido
                if active is not None:
                    self.alerts[i]['active'] = active
                
                # Atualizar data de modificação
                self.alerts[i]['updated_at'] = datetime.now().isoformat()
                
                # Salvar lista atualizada
                self.save_alerts()
                
                return True
        
        logger.warning(f"Alerta não encontrado: {alert_id}")
        return False
    
    def delete_alert(self, alert_id):
        """
        Remove um alerta.
        
        Args:
            alert_id (str): ID do alerta
            
        Returns:
            bool: True se removido com sucesso, False caso contrário
        """
        logger.info(f"Removendo alerta: {alert_id}")
        
        # Procurar alerta
        for i, alert in enumerate(self.alerts):
            if alert.get('id') == alert_id:
                # Remover da lista
                del self.alerts[i]
                
                # Salvar lista atualizada
                self.save_alerts()
                
                return True
        
        logger.warning(f"Alerta não encontrado: {alert_id}")
        return False
    
    def check_alerts(self, stock_data):
        """
        Verifica alertas para uma ação específica.
        
        Args:
            stock_data (dict): Dados da ação
            
        Returns:
            list: Alertas disparados
        """
        logger.info(f"Verificando alertas para {stock_data.get('symbol', '')}")
        
        triggered_alerts = []
        symbol = stock_data.get('symbol', '')
        price = stock_data.get('price', 0)
        
        # Verificar cada alerta
        for alert in self.alerts:
            # Ignorar alertas inativos
            if not alert.get('active', True):
                continue
            
            # Verificar se o alerta é para esta ação
            if alert.get('params', {}).get('symbol') != symbol:
                continue
            
            alert_type = alert.get('type', '')
            params = alert.get('params', {})
            
            # Alerta de preço
            if alert_type == 'price':
                condition = params.get('condition', '>')
                target_price = params.get('price', 0)
                
                if (condition == '>' and price > target_price) or \
                   (condition == '<' and price < target_price) or \
                   (condition == '=' and abs(price - target_price) < 0.01):
                    triggered_alerts.append(alert)
                    
                    # Atualizar data do último disparo
                    alert['last_triggered'] = datetime.now().isoformat()
            
            # Alerta de preço-alvo
            elif alert_type == 'target':
                target_price = params.get('target_price', 0)
                threshold = params.get('threshold', 0.05)  # 5% de tolerância
                
                if abs(price - target_price) / target_price <= threshold:
                    triggered_alerts.append(alert)
                    
                    # Atualizar data do último disparo
                    alert['last_triggered'] = datetime.now().isoformat()
            
            # Alerta de oportunidade
            elif alert_type == 'opportunity':
                fair_value = stock_data.get('graham_value', {}).get('fair_value', 0)
                threshold = params.get('threshold', 0.7)  # 70% do valor justo
                
                if price <= threshold * fair_value:
                    triggered_alerts.append(alert)
                    
                    # Atualizar data do último disparo
                    alert['last_triggered'] = datetime.now().isoformat()
        
        # Salvar alertas atualizados
        if triggered_alerts:
            self.save_alerts()
        
        return triggered_alerts
    
    def send_alert_notifications(self, triggered_alerts, stock_data):
        """
        Envia notificações para alertas disparados.
        
        Args:
            triggered_alerts (list): Alertas disparados
            stock_data (dict): Dados da ação
            
        Returns:
            int: Número de notificações enviadas
        """
        logger.info(f"Enviando notificações para {len(triggered_alerts)} alertas")
        
        sent_count = 0
        symbol = stock_data.get('symbol', '')
        name = stock_data.get('name', '')
        price = stock_data.get('price', 0)
        
        for alert in triggered_alerts:
            user_id = alert.get('user_id', '')
            alert_type = alert.get('type', '')
            params = alert.get('params', {})
            
            # Construir mensagem
            message = f"🔔 *Alerta Clearview Capital* 🔔\n\n"
            message += f"*{symbol} - {name}*\n\n"
            
            if alert_type == 'price':
                condition = params.get('condition', '>')
                target_price = params.get('price', 0)
                
                condition_text = "atingiu" if condition == '=' else \
                                "ultrapassou" if condition == '>' else "caiu abaixo de"
                
                message += f"O preço {condition_text} R$ {target_price:.2f}\n"
                message += f"Preço atual: R$ {price:.2f}\n"
            
            elif alert_type == 'target':
                target_price = params.get('target_price', 0)
                
                message += f"O preço está próximo do alvo de R$ {target_price:.2f}\n"
                message += f"Preço atual: R$ {price:.2f}\n"
            
            elif alert_type == 'opportunity':
                fair_value = stock_data.get('graham_value', {}).get('fair_value', 0)
                threshold = params.get('threshold', 0.7)
                
                message += f"Oportunidade de compra detectada!\n"
                message += f"Preço atual: R$ {price:.2f}\n"
                message += f"Valor justo: R$ {fair_value:.2f}\n"
                message += f"A ação está sendo negociada a {(price/fair_value*100):.1f}% do valor justo\n"
            
            message += f"\nAcesse a plataforma para mais detalhes."
            
            # Enviar notificação por diferentes canais
            
            # Telegram
            if self.config.get('telegram', {}).get('enabled', False):
                self.send_telegram_notification(message, user_id=user_id)
                sent_count += 1
            
            # E-mail
            if self.config.get('email', {}).get('enabled', False):
                # Buscar e-mail do usuário (em uma implementação real, seria buscado no banco de dados)
                email = f"{user_id}@example.com"  # Placeholder
                
                subject = f"Alerta Clearview Capital - {symbol}"
                self.send_email(email, subject, message)
                sent_count += 1
            
            # Notificação push
            if self.config.get('push', {}).get('enabled', False):
                self.send_push_notification(user_id, message)
                sent_count += 1
            
            # Notificação na plataforma
            if self.config.get('platform', {}).get('enabled', False):
                self.save_platform_notification(user_id, message)
                sent_count += 1
            
            # Registrar no histórico
            self.notification_history.append({
                'user_id': user_id,
                'alert_id': alert.get('id', ''),
                'type': alert_type,
                'message': message,
                'date': datetime.now().isoformat()
            })
        
        # Salvar histórico atualizado
        if sent_count > 0:
            self.save_notification_history()
        
        return sent_count
    
    def send_welcome_email(self, email, name=""):
        """
        Envia e-mail de boas-vindas para novo assinante.
        
        Args:
            email (str): E-mail do assinante
            name (str): Nome do assinante
            
        Returns:
            bool: True se enviado com sucesso, False caso contrário
        """
        logger.info(f"Enviando e-mail de boas-vindas para {email}")
        
        # Personalizar saudação
        greeting = f"Olá, {name}" if name else "Olá"
        
        # Construir assunto
        subject = "Bem-vindo à Newsletter da Clearview Capital"
        
        # Construir conteúdo HTML
        content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{subject}</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                .header {{
                    text-align: center;
                    margin-bottom: 30px;
                }}
                .logo {{
                    max-width: 200px;
                }}
                h1, h2 {{
                    color: #0047AB;
                }}
                .content {{
                    margin-bottom: 30px;
                    padding: 20px;
                    background-color: #f9f9f9;
                    border-radius: 5px;
                }}
                .footer {{
                    text-align: center;
                    margin-top: 30px;
                    font-size: 12px;
                    color: #777;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <img src="https://clearview-capital.com/logo.png" alt="Clearview Capital" class="logo">
                <h1>Bem-vindo à Clearview Capital</h1>
            </div>
            
            <div class="content">
                <p>{greeting},</p>
                
                <p>Seja bem-vindo à newsletter da <strong>Clearview Capital</strong>!</p>
                
                <p>A partir de agora, você receberá diariamente:</p>
                <ul>
                    <li>Análises de mercado</li>
                    <li>Recomendações de investimentos</li>
                    <li>Oportunidades identificadas por nossa IA</li>
                    <li>Notícias relevantes do mundo financeiro</li>
                </ul>
                
                <p>Nossa plataforma utiliza inteligência artificial para analisar o mercado e identificar as melhores oportunidades de investimento com base em critérios fundamentalistas.</p>
                
                <p>Fique atento à sua caixa de entrada para receber nossa primeira newsletter!</p>
                
                <p>Atenciosamente,<br>
                Equipe Clearview Capital</p>
            </div>
            
            <div class="footer">
                <p>© Clearview Capital. Todos os direitos reservados.</p>
                <p>Para cancelar a inscrição, <a href="#">clique aqui</a>.</p>
            </div>
        </body>
        </html>
        """
        
        # Enviar e-mail
        return self.send_email(email, subject, content)
    
    def send_unsubscribe_confirmation(self, email, name=""):
        """
        Envia e-mail de confirmação de cancelamento de inscrição.
        
        Args:
            email (str): E-mail do assinante
            name (str): Nome do assinante
            
        Returns:
            bool: True se enviado com sucesso, False caso contrário
        """
        logger.info(f"Enviando confirmação de cancelamento para {email}")
        
        # Personalizar saudação
        greeting = f"Olá, {name}" if name else "Olá"
        
        # Construir assunto
        subject = "Confirmação de cancelamento da Newsletter da Clearview Capital"
        
        # Construir conteúdo HTML
        content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{subject}</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                .header {{
                    text-align: center;
                    margin-bottom: 30px;
                }}
                .logo {{
                    max-width: 200px;
                }}
                h1, h2 {{
                    color: #0047AB;
                }}
                .content {{
                    margin-bottom: 30px;
                    padding: 20px;
                    background-color: #f9f9f9;
                    border-radius: 5px;
                }}
                .footer {{
                    text-align: center;
                    margin-top: 30px;
                    font-size: 12px;
                    color: #777;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <img src="https://clearview-capital.com/logo.png" alt="Clearview Capital" class="logo">
                <h1>Cancelamento Confirmado</h1>
            </div>
            
            <div class="content">
                <p>{greeting},</p>
                
                <p>Confirmamos o cancelamento da sua inscrição na newsletter da <strong>Clearview Capital</strong>.</p>
                
                <p>Sentimos muito por vê-lo partir. Se quiser compartilhar o motivo do cancelamento ou sugerir melhorias, basta responder a este e-mail.</p>
                
                <p>Caso mude de ideia, você pode se inscrever novamente a qualquer momento em nosso site.</p>
                
                <p>Atenciosamente,<br>
                Equipe Clearview Capital</p>
            </div>
            
            <div class="footer">
                <p>© Clearview Capital. Todos os direitos reservados.</p>
                <p>Para se inscrever novamente, <a href="#">clique aqui</a>.</p>
            </div>
        </body>
        </html>
        """
        
        # Enviar e-mail
        return self.send_email(email, subject, content)
    
    def send_daily_newsletter(self, market_data, portfolio, favorites, news):
        """
        Envia a newsletter diária para todos os assinantes ativos.
        
        Args:
            market_data (dict): Dados do mercado
            portfolio (dict): Dados da carteira
            favorites (list): Lista de ações favoritas
            news (list): Lista de notícias
            
        Returns:
            int: Número de newsletters enviadas
        """
        logger.info("Enviando newsletter diária")
        
        # Gerar newsletter
        newsletter = self.ai.generate_daily_newsletter(market_data, portfolio, favorites, news)
        
        sent_count = 0
        
        # Enviar para cada assinante ativo
        for subscriber in self.subscribers:
            if subscriber.get('active', True):
                email = subscriber.get('email', '')
                name = subscriber.get('name', '')
                
                # Personalizar newsletter com nome do assinante
                personalized_content = newsletter['content'].replace("{{name}}", name if name else "Investidor")
                
                # Enviar e-mail
                if self.send_email(email, newsletter['subject'], personalized_content):
                    sent_count += 1
        
        logger.info(f"Newsletter enviada para {sent_count} assinantes")
        
        return sent_count
    
    def send_email(self, to_email, subject, content):
        """
        Envia um e-mail.
        
        Args:
            to_email (str): E-mail do destinatário
            subject (str): Assunto do e-mail
            content (str): Conteúdo do e-mail (HTML)
            
        Returns:
            bool: True se enviado com sucesso, False caso contrário
        """
        logger.info(f"Enviando e-mail para {to_email}: {subject}")
        
        # Em uma implementação real, usaríamos SMTP
        # Para este exemplo, vamos simular o envio
        
        # Verificar se o e-mail está habilitado
        if not self.config.get('email', {}).get('enabled', False):
            logger.warning("Envio de e-mail desabilitado nas configurações")
            return False
        
        # Obter configurações de SMTP
        smtp_server = self.config.get('email', {}).get('smtp_server', '')
        smtp_port = self.config.get('email', {}).get('smtp_port', 587)
        smtp_user = self.config.get('email', {}).get('smtp_user', '')
        smtp_password = self.config.get('email', {}).get('smtp_password', '')
        from_name = self.config.get('email', {}).get('from_name', 'Clearview Capital')
        
        # Verificar se temos todas as configurações necessárias
        if not all([smtp_server, smtp_port, smtp_user]):
            logger.error("Configurações de SMTP incompletas")
            return False
        
        # Em uma implementação real, seria algo como:
        """
        try:
            # Configurar servidor SMTP
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(smtp_user, smtp_password)
            
            # Criar mensagem
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = f"{from_name} <{smtp_user}>"
            msg['To'] = to_email
            
            # Adicionar conteúdo HTML
            msg.attach(MIMEText(content, 'html'))
            
            # Enviar e-mail
            server.sendmail(smtp_user, to_email, msg.as_string())
            
            # Fechar conexão
            server.quit()
            
            logger.info(f"E-mail enviado com sucesso para {to_email}")
            return True
        except Exception as e:
            logger.error(f"Erro ao enviar e-mail: {e}")
            return False
        """
        
        # Simular envio bem-sucedido
        logger.info(f"E-mail enviado com sucesso para {to_email}")
        return True
    
    def send_telegram_notification(self, message, chat_id=None, user_id=None):
        """
        Envia notificação via Telegram.
        
        Args:
            message (str): Mensagem a ser enviada
            chat_id (str): ID do chat ou canal
            user_id (str): ID do usuário (para buscar chat_id)
            
        Returns:
            bool: True se enviado com sucesso, False caso contrário
        """
        logger.info("Enviando notificação via Telegram")
        
        # Verificar se o Telegram está habilitado
        if not self.config.get('telegram', {}).get('enabled', False):
            logger.warning("Telegram desabilitado nas configurações")
            return False
        
        # Obter token do bot
        bot_token = self.config.get('telegram', {}).get('bot_token', '')
        
        if not bot_token:
            logger.error("Token do bot Telegram não configurado")
            return False
        
        # Se user_id for fornecido, buscar chat_id correspondente
        # Em uma implementação real, seria buscado em um banco de dados
        if user_id and not chat_id:
            # Placeholder
            chat_id = f"user_{user_id}"
        
        # Se chat_id não for fornecido, usar canal padrão
        if not chat_id:
            chat_id = self.config.get('telegram', {}).get('channel_id', '')
        
        # Em uma implementação real, seria algo como:
        """
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "Markdown"
        }
        
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                logger.info(f"Notificação enviada com sucesso para {chat_id}")
                return True
            else:
                logger.error(f"Erro ao enviar notificação: {response.text}")
                return False
        except Exception as e:
            logger.error(f"Erro ao enviar notificação: {e}")
            return False
        """
        
        # Simular envio bem-sucedido
        logger.info(f"Notificação enviada com sucesso para {chat_id}")
        return True
    
    def send_push_notification(self, user_id, message, title=None):
        """
        Envia notificação push para o navegador.
        
        Args:
            user_id (str): ID do usuário
            message (str): Mensagem a ser enviada
            title (str): Título da notificação
            
        Returns:
            bool: True se enviado com sucesso, False caso contrário
        """
        logger.info(f"Enviando notificação push para usuário {user_id}")
        
        # Verificar se as notificações push estão habilitadas
        if not self.config.get('push', {}).get('enabled', False):
            logger.warning("Notificações push desabilitadas nas configurações")
            return False
        
        # Em uma implementação real, buscaríamos as inscrições push do usuário
        # e enviaríamos a notificação usando Web Push API
        
        # Simular envio bem-sucedido
        logger.info(f"Notificação push enviada com sucesso para usuário {user_id}")
        return True
    
    def save_platform_notification(self, user_id, message, title=None, link=None):
        """
        Salva uma notificação na plataforma para ser exibida ao usuário.
        
        Args:
            user_id (str): ID do usuário
            message (str): Mensagem a ser enviada
            title (str): Título da notificação
            link (str): Link para redirecionamento
            
        Returns:
            bool: True se salvo com sucesso, False caso contrário
        """
        logger.info(f"Salvando notificação na plataforma para usuário {user_id}")
        
        # Verificar se as notificações na plataforma estão habilitadas
        if not self.config.get('platform', {}).get('enabled', False):
            logger.warning("Notificações na plataforma desabilitadas nas configurações")
            return False
        
        # Em uma implementação real, salvaríamos a notificação em um banco de dados
        # para ser exibida quando o usuário acessar a plataforma
        
        # Simular salvamento bem-sucedido
        logger.info(f"Notificação salva com sucesso para usuário {user_id}")
        return True
    
    def run_scheduled_tasks(self):
        """
        Executa tarefas agendadas (newsletter diária, alertas de mercado, etc.).
        
        Returns:
            dict: Resultados das tarefas executadas
        """
        logger.info("Executando tarefas agendadas")
        
        results = {
            'daily_newsletter': 0,
            'market_open_alert': 0,
            'market_close_alert': 0,
            'opportunity_check': 0
        }
        
        # Obter hora atual
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        
        # Verificar se é hora de enviar a newsletter diária
        newsletter_time = self.config.get('schedule', {}).get('daily_newsletter', '18:00')
        if current_time == newsletter_time:
            # Em uma implementação real, buscaríamos dados atualizados
            # Para este exemplo, vamos simular
            market_data = {}
            portfolio = {}
            favorites = []
            news = []
            
            # Enviar newsletter
            results['daily_newsletter'] = self.send_daily_newsletter(market_data, portfolio, favorites, news)
        
        # Verificar se é hora de enviar alerta de abertura do mercado
        market_open_time = self.config.get('schedule', {}).get('market_open_alert', '10:00')
        if current_time == market_open_time:
            # Enviar alerta de abertura do mercado
            message = "🔔 *Mercado Aberto* 🔔\n\n"
            message += "O mercado está aberto para negociações.\n\n"
            message += "Acesse a plataforma para acompanhar as movimentações em tempo real."
            
            # Enviar para todos os assinantes
            for subscriber in self.subscribers:
                if subscriber.get('active', True):
                    email = subscriber.get('email', '')
                    
                    if self.send_email(email, "Mercado Aberto - Clearview Capital", message):
                        results['market_open_alert'] += 1
        
        # Verificar se é hora de enviar alerta de fechamento do mercado
        market_close_time = self.config.get('schedule', {}).get('market_close_alert', '17:30')
        if current_time == market_close_time:
            # Enviar alerta de fechamento do mercado
            message = "🔔 *Mercado Fechado* 🔔\n\n"
            message += "O mercado está fechado para negociações.\n\n"
            message += "Acesse a plataforma para ver o resumo do dia e as recomendações para amanhã."
            
            # Enviar para todos os assinantes
            for subscriber in self.subscribers:
                if subscriber.get('active', True):
                    email = subscriber.get('email', '')
                    
                    if self.send_email(email, "Mercado Fechado - Clearview Capital", message):
                        results['market_close_alert'] += 1
        
        # Verificar se é hora de verificar oportunidades
        opportunity_check_times = self.config.get('schedule', {}).get('opportunity_check', '12:00,15:00').split(',')
        if current_time in opportunity_check_times:
            # Em uma implementação real, buscaríamos dados atualizados
            # Para este exemplo, vamos simular
            
            # Simular verificação de oportunidades
            results['opportunity_check'] = 3  # Número de oportunidades encontradas
        
        return results

# Função principal para teste
def main():
    notification_system = NotificationSystem()
    
    # Adicionar assinante de teste
    notification_system.add_subscriber("teste@example.com", "Usuário Teste")
    
    # Criar alerta de teste
    alert_id = notification_system.create_alert(
        user_id="user123",
        alert_type="price",
        params={
            "symbol": "PETR4",
            "condition": ">",
            "price": 30.0
        }
    )
    
    # Simular dados de ação
    stock_data = {
        'symbol': 'PETR4',
        'name': 'PETROBRAS PN',
        'price': 36.75,
        'change_1d': 2.15,
        'graham_value': {
            'fair_value': 42.30,
            'potential': 15.1
        }
    }
    
    # Verificar alertas
    triggered_alerts = notification_system.check_alerts(stock_data)
    
    # Enviar notificações
    sent_count = notification_system.send_alert_notifications(triggered_alerts, stock_data)
    
    print(f"Alertas disparados: {len(triggered_alerts)}")
    print(f"Notificações enviadas: {sent_count}")
    
    # Executar tarefas agendadas
    results = notification_system.run_scheduled_tasks()
    print(f"Resultados das tarefas agendadas: {results}")

if __name__ == "__main__":
    main()
