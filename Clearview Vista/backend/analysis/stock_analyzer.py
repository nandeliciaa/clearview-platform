#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Módulo de análise financeira para a Plataforma Inteligente da Clearview Capital.
Este módulo implementa a coleta de dados financeiros, cálculo de indicadores
fundamentalistas e aplicação da fórmula de Graham para avaliação de ações.
"""

import sys
import os
import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import requests
import logging

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("stock_analyzer.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("StockAnalyzer")

# Adicionar o caminho para as APIs de dados
sys.path.append('/opt/.manus/.sandbox-runtime')

try:
    from data_api import ApiClient
    logger.info("API Client importado com sucesso")
except ImportError as e:
    logger.error(f"Erro ao importar API Client: {e}")
    # Fallback para APIs públicas se o módulo data_api não estiver disponível
    pass

class StockAnalyzer:
    """
    Classe principal para análise de ações com base em indicadores fundamentalistas.
    Implementa a coleta de dados, cálculo de indicadores e avaliação de ações.
    """
    
    def __init__(self, data_dir="/home/ubuntu/clearview_project/data"):
        """
        Inicializa o analisador de ações.
        
        Args:
            data_dir (str): Diretório para armazenamento de dados
        """
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
        
        # Inicializar cliente de API
        try:
            self.api_client = ApiClient()
            logger.info("API Client inicializado")
        except:
            self.api_client = None
            logger.warning("API Client não disponível, usando APIs públicas")
        
        # Dicionário para armazenar dados de ações
        self.stocks_data = {}
        
        # Lista de ações brasileiras para monitorar
        self.br_stocks = [
            "PETR4", "VALE3", "ITUB4", "BBDC4", "ABEV3", 
            "WEGE3", "RENT3", "BBAS3", "EGIE3", "TAEE11"
        ]
        
        # Lista de ações americanas para monitorar
        self.us_stocks = [
            "AAPL", "MSFT", "AMZN", "GOOGL", "META", 
            "TSLA", "NVDA", "BRK-B", "JPM", "JNJ"
        ]
        
        # Carregar dados salvos, se existirem
        self.load_data()
    
    def load_data(self):
        """Carrega dados salvos de ações, se existirem."""
        try:
            stocks_file = os.path.join(self.data_dir, "stocks_data.json")
            if os.path.exists(stocks_file):
                with open(stocks_file, 'r', encoding='utf-8') as f:
                    self.stocks_data = json.load(f)
                logger.info(f"Dados carregados de {stocks_file}")
        except Exception as e:
            logger.error(f"Erro ao carregar dados: {e}")
    
    def save_data(self):
        """Salva dados de ações em arquivo JSON."""
        try:
            stocks_file = os.path.join(self.data_dir, "stocks_data.json")
            with open(stocks_file, 'w', encoding='utf-8') as f:
                json.dump(self.stocks_data, f, ensure_ascii=False, indent=2)
            logger.info(f"Dados salvos em {stocks_file}")
        except Exception as e:
            logger.error(f"Erro ao salvar dados: {e}")
    
    def fetch_stock_data(self, symbol, region="BR"):
        """
        Busca dados de uma ação específica.
        
        Args:
            symbol (str): Código da ação
            region (str): Região da ação (BR ou US)
            
        Returns:
            dict: Dados da ação
        """
        logger.info(f"Buscando dados para {symbol} na região {region}")
        
        stock_data = {}
        
        # Determinar região correta para a API
        api_region = "BR" if region == "BR" else "US"
        
        # Buscar dados de cotação
        try:
            if self.api_client:
                # Usar API interna se disponível
                chart_data = self.api_client.call_api(
                    'YahooFinance/get_stock_chart', 
                    query={
                        'symbol': symbol,
                        'region': api_region,
                        'interval': '1d',
                        'range': '1y'
                    }
                )
                
                if chart_data and 'chart' in chart_data and 'result' in chart_data['chart']:
                    result = chart_data['chart']['result'][0]
                    
                    # Extrair metadados
                    meta = result['meta']
                    stock_data['symbol'] = symbol
                    stock_data['currency'] = meta.get('currency')
                    stock_data['exchange'] = meta.get('exchangeName')
                    stock_data['name'] = meta.get('shortName', '')
                    stock_data['long_name'] = meta.get('longName', '')
                    
                    # Extrair preços
                    quotes = result['indicators']['quote'][0]
                    timestamps = result['timestamp']
                    
                    # Obter último preço disponível
                    last_valid_idx = -1
                    for i in range(len(quotes['close'])-1, -1, -1):
                        if quotes['close'][i] is not None:
                            last_valid_idx = i
                            break
                    
                    if last_valid_idx >= 0:
                        stock_data['price'] = quotes['close'][last_valid_idx]
                        stock_data['last_update'] = timestamps[last_valid_idx]
                        
                        # Calcular variação em 1 dia
                        if last_valid_idx > 0 and quotes['close'][last_valid_idx-1] is not None:
                            prev_price = quotes['close'][last_valid_idx-1]
                            stock_data['change_1d'] = (stock_data['price'] - prev_price) / prev_price * 100
                        else:
                            stock_data['change_1d'] = 0
                        
                        # Calcular variação em 1 ano
                        first_valid_idx = 0
                        for i in range(len(quotes['close'])):
                            if quotes['close'][i] is not None:
                                first_valid_idx = i
                                break
                        
                        if first_valid_idx < last_valid_idx:
                            first_price = quotes['close'][first_valid_idx]
                            stock_data['change_1y'] = (stock_data['price'] - first_price) / first_price * 100
                        else:
                            stock_data['change_1y'] = 0
                
                # Buscar insights e indicadores fundamentalistas
                insights_data = self.api_client.call_api(
                    'YahooFinance/get_stock_insights', 
                    query={'symbol': symbol}
                )
                
                if insights_data and 'finance' in insights_data and 'result' in insights_data['finance']:
                    result = insights_data['finance']['result']
                    
                    # Extrair indicadores técnicos
                    if 'instrumentInfo' in result and 'technicalEvents' in result['instrumentInfo']:
                        tech_events = result['instrumentInfo']['technicalEvents']
                        stock_data['technical_outlook'] = {
                            'short_term': tech_events.get('shortTermOutlook', {}).get('direction', ''),
                            'mid_term': tech_events.get('intermediateTermOutlook', {}).get('direction', ''),
                            'long_term': tech_events.get('longTermOutlook', {}).get('direction', '')
                        }
                    
                    # Extrair recomendação
                    if 'recommendation' in result:
                        stock_data['recommendation'] = {
                            'rating': result['recommendation'].get('rating', ''),
                            'target_price': result['recommendation'].get('targetPrice', None)
                        }
            else:
                # Usar API pública como fallback
                # Implementação de fallback usando requests para Yahoo Finance API pública
                logger.warning("Usando API pública como fallback")
                pass
                
        except Exception as e:
            logger.error(f"Erro ao buscar dados para {symbol}: {e}")
        
        return stock_data
    
    def fetch_fundamentals(self, symbol, region="BR"):
        """
        Busca indicadores fundamentalistas para uma ação.
        
        Args:
            symbol (str): Código da ação
            region (str): Região da ação (BR ou US)
            
        Returns:
            dict: Indicadores fundamentalistas
        """
        # Aqui seria implementada a busca de indicadores fundamentalistas
        # Como exemplo, vamos criar alguns indicadores simulados
        
        # Em uma implementação real, esses dados viriam de APIs financeiras
        fundamentals = {
            'P/L': round(np.random.uniform(5, 30), 2),
            'P/VP': round(np.random.uniform(0.5, 5), 2),
            'ROE': round(np.random.uniform(5, 25), 2),
            'Dividend Yield': round(np.random.uniform(0, 10), 2),
            'Dívida/EBITDA': round(np.random.uniform(0, 3), 2),
            'Margem Líquida': round(np.random.uniform(5, 30), 2),
            'Margem EBITDA': round(np.random.uniform(10, 40), 2),
            'Crescimento Receita (5 anos)': round(np.random.uniform(0, 20), 2),
        }
        
        return fundamentals
    
    def calculate_graham_value(self, symbol, fundamentals):
        """
        Calcula o valor justo de uma ação usando a fórmula de Graham.
        
        Fórmula de Graham: √(22.5 * LPA * VPA)
        Onde:
        - LPA = Lucro por Ação
        - VPA = Valor Patrimonial por Ação
        
        Args:
            symbol (str): Código da ação
            fundamentals (dict): Indicadores fundamentalistas
            
        Returns:
            float: Valor justo calculado
        """
        # Em uma implementação real, esses valores viriam dos dados fundamentalistas
        # Para este exemplo, vamos simular
        
        # Obter preço atual
        current_price = self.stocks_data.get(symbol, {}).get('price', 100)
        
        # Simular LPA e VPA
        pe_ratio = fundamentals.get('P/L', 15)
        pb_ratio = fundamentals.get('P/VP', 2)
        
        # Calcular LPA e VPA a partir dos múltiplos
        lpa = current_price / pe_ratio if pe_ratio > 0 else 0
        vpa = current_price / pb_ratio if pb_ratio > 0 else 0
        
        # Aplicar fórmula de Graham
        if lpa > 0 and vpa > 0:
            graham_value = np.sqrt(22.5 * lpa * vpa)
        else:
            graham_value = current_price  # Fallback se não for possível calcular
        
        # Calcular potencial de valorização
        potential = ((graham_value - current_price) / current_price) * 100
        
        return {
            'fair_value': round(graham_value, 2),
            'potential': round(potential, 2),
            'lpa': round(lpa, 2),
            'vpa': round(vpa, 2)
        }
    
    def evaluate_stock(self, symbol, fundamentals, graham_value):
        """
        Avalia uma ação com base em critérios fundamentalistas e valor de Graham.
        
        Args:
            symbol (str): Código da ação
            fundamentals (dict): Indicadores fundamentalistas
            graham_value (dict): Valor justo e potencial
            
        Returns:
            dict: Avaliação da ação
        """
        # Critérios para avaliação
        evaluation = {
            'rating': 'Neutro',
            'strengths': [],
            'weaknesses': [],
            'opportunity': False,
            'score': 0
        }
        
        score = 0
        
        # Avaliar P/L
        pl = fundamentals.get('P/L', 0)
        if pl > 0:
            if pl < 10:
                score += 2
                evaluation['strengths'].append('P/L baixo, indicando possível subavaliação')
            elif pl > 25:
                score -= 2
                evaluation['weaknesses'].append('P/L alto, indicando possível sobreavaliação')
        
        # Avaliar P/VP
        pvp = fundamentals.get('P/VP', 0)
        if pvp > 0:
            if pvp < 1:
                score += 2
                evaluation['strengths'].append('P/VP abaixo de 1, indicando possível subavaliação')
            elif pvp > 3:
                score -= 1
                evaluation['weaknesses'].append('P/VP alto, indicando possível sobreavaliação')
        
        # Avaliar ROE
        roe = fundamentals.get('ROE', 0)
        if roe > 15:
            score += 2
            evaluation['strengths'].append('ROE alto, indicando boa rentabilidade')
        elif roe < 8:
            score -= 1
            evaluation['weaknesses'].append('ROE baixo, indicando rentabilidade abaixo da média')
        
        # Avaliar Dividend Yield
        dy = fundamentals.get('Dividend Yield', 0)
        if dy > 6:
            score += 2
            evaluation['strengths'].append('Dividend Yield atrativo')
        
        # Avaliar Dívida/EBITDA
        debt_ebitda = fundamentals.get('Dívida/EBITDA', 0)
        if debt_ebitda < 1.5:
            score += 1
            evaluation['strengths'].append('Baixo endividamento')
        elif debt_ebitda > 3:
            score -= 2
            evaluation['weaknesses'].append('Alto endividamento')
        
        # Avaliar potencial de Graham
        potential = graham_value.get('potential', 0)
        if potential > 30:
            score += 3
            evaluation['strengths'].append('Alto potencial segundo fórmula de Graham')
            evaluation['opportunity'] = True
        elif potential > 15:
            score += 2
            evaluation['strengths'].append('Bom potencial segundo fórmula de Graham')
        elif potential < -15:
            score -= 2
            evaluation['weaknesses'].append('Potencial negativo segundo fórmula de Graham')
        
        # Determinar rating com base no score
        evaluation['score'] = score
        if score >= 5:
            evaluation['rating'] = 'Compra'
        elif score >= 2:
            evaluation['rating'] = 'Manter'
        elif score <= -3:
            evaluation['rating'] = 'Venda'
        else:
            evaluation['rating'] = 'Neutro'
        
        # Verificar se é uma ótima oportunidade (70% do valor justo)
        current_price = self.stocks_data.get(symbol, {}).get('price', 0)
        fair_value = graham_value.get('fair_value', 0)
        
        if current_price > 0 and fair_value > 0:
            if current_price <= 0.7 * fair_value:
                evaluation['opportunity'] = True
                evaluation['strengths'].append('Cotada abaixo de 70% do valor justo')
        
        return evaluation
    
    def update_portfolio(self):
        """
        Atualiza a carteira da Clearview Capital com base nas análises.
        
        Returns:
            dict: Nova composição da carteira
        """
        portfolio = {
            'stocks': [],
            'last_update': datetime.now().isoformat(),
            'total_score': 0
        }
        
        # Analisar todas as ações monitoradas
        all_stocks = self.br_stocks + self.us_stocks
        analyzed_stocks = []
        
        for symbol in all_stocks:
            region = "US" if symbol in self.us_stocks else "BR"
            
            # Verificar se já temos dados recentes
            stock_data = self.stocks_data.get(symbol, {})
            last_update = stock_data.get('last_update', 0)
            
            # Se os dados têm mais de 1 dia, atualizar
            if time.time() - last_update > 86400:  # 24 horas em segundos
                stock_data = self.fetch_stock_data(symbol, region)
                self.stocks_data[symbol] = stock_data
            
            # Buscar ou simular fundamentals
            fundamentals = self.fetch_fundamentals(symbol, region)
            
            # Calcular valor de Graham
            graham_value = self.calculate_graham_value(symbol, fundamentals)
            
            # Avaliar ação
            evaluation = self.evaluate_stock(symbol, fundamentals, graham_value)
            
            # Adicionar à lista de ações analisadas
            analyzed_stocks.append({
                'symbol': symbol,
                'name': stock_data.get('name', ''),
                'price': stock_data.get('price', 0),
                'change_1d': stock_data.get('change_1d', 0),
                'fundamentals': fundamentals,
                'graham_value': graham_value,
                'evaluation': evaluation,
                'region': region
            })
        
        # Salvar dados atualizados
        self.save_data()
        
        # Selecionar ações para a carteira (as com melhor avaliação)
        analyzed_stocks.sort(key=lambda x: x['evaluation']['score'], reverse=True)
        
        # Selecionar as 10 melhores ações, com pelo menos 7 brasileiras
        br_count = 0
        portfolio_stocks = []
        
        for stock in analyzed_stocks:
            if len(portfolio_stocks) < 10:
                if stock['region'] == 'BR':
                    br_count += 1
                portfolio_stocks.append(stock)
            elif br_count < 7 and stock['region'] == 'BR':
                # Substituir a pior ação internacional por uma brasileira
                for i in range(len(portfolio_stocks)-1, -1, -1):
                    if portfolio_stocks[i]['region'] == 'US':
                        portfolio_stocks[i] = stock
                        br_count += 1
                        break
        
        portfolio['stocks'] = portfolio_stocks
        portfolio['total_score'] = sum(stock['evaluation']['score'] for stock in portfolio_stocks)
        
        # Salvar a carteira em um arquivo separado
        try:
            portfolio_file = os.path.join(self.data_dir, "portfolio.json")
            with open(portfolio_file, 'w', encoding='utf-8') as f:
                json.dump(portfolio, f, ensure_ascii=False, indent=2)
            logger.info(f"Carteira salva em {portfolio_file}")
        except Exception as e:
            logger.error(f"Erro ao salvar carteira: {e}")
        
        return portfolio
    
    def get_favorites(self):
        """
        Retorna as ações favoritas (melhores oportunidades).
        
        Returns:
            list: Lista de ações favoritas
        """
        favorites = []
        
        # Carregar dados da carteira
        try:
            portfolio_file = os.path.join(self.data_dir, "portfolio.json")
            if os.path.exists(portfolio_file):
                with open(portfolio_file, 'r', encoding='utf-8') as f:
                    portfolio = json.load(f)
                
                # Filtrar ações marcadas como oportunidades
                for stock in portfolio.get('stocks', []):
                    if stock.get('evaluation', {}).get('opportunity', False):
                        favorites.append(stock)
        except Exception as e:
            logger.error(f"Erro ao carregar favoritas: {e}")
        
        # Ordenar por potencial
        favorites.sort(key=lambda x: x.get('graham_value', {}).get('potential', 0), reverse=True)
        
        return favorites
    
    def generate_report(self, stock):
        """
        Gera um relatório em linguagem natural para uma ação.
        
        Args:
            stock (dict): Dados da ação
            
        Returns:
            str: Relatório em texto
        """
        symbol = stock.get('symbol', '')
        name = stock.get('name', '')
        price = stock.get('price', 0)
        change = stock.get('change_1d', 0)
        
        fundamentals = stock.get('fundamentals', {})
        graham = stock.get('graham_value', {})
        evaluation = stock.get('evaluation', {})
        
        # Construir relatório
        report = f"Análise de {symbol} - {name}\n\n"
        
        # Resumo
        report += "Resumo:\n"
        report += f"Cotação atual: {price:.2f} ({'+' if change >= 0 else ''}{change:.2f}%)\n"
        report += f"Valor justo (Graham): {graham.get('fair_value', 0):.2f}\n"
        report += f"Potencial: {'+' if graham.get('potential', 0) >= 0 else ''}{graham.get('potential', 0):.2f}%\n"
        report += f"Avaliação: {evaluation.get('rating', 'Neutro')}\n\n"
        
        # Indicadores
        report += "Indicadores Fundamentalistas:\n"
        for key, value in fundamentals.items():
            report += f"- {key}: {value}\n"
        report += "\n"
        
        # Pontos fortes e fracos
        report += "Pontos Fortes:\n"
        for strength in evaluation.get('strengths', []):
            report += f"- {strength}\n"
        
        if not evaluation.get('strengths'):
            report += "- Nenhum ponto forte identificado\n"
        
        report += "\nPontos Fracos:\n"
        for weakness in evaluation.get('weaknesses', []):
            report += f"- {weakness}\n"
        
        if not evaluation.get('weaknesses'):
            report += "- Nenhum ponto fraco identificado\n"
        
        # Conclusão
        report += "\nConclusão:\n"
        if evaluation.get('rating') == 'Compra':
            report += f"{symbol} apresenta bons fundamentos e está com preço atrativo. "
            report += "Recomendamos a compra para investidores de longo prazo."
        elif evaluation.get('rating') == 'Manter':
            report += f"{symbol} apresenta fundamentos adequados ao preço atual. "
            report += "Recomendamos manter para quem já possui a ação."
        elif evaluation.get('rating') == 'Venda':
            report += f"{symbol} apresenta fundamentos fracos ou está sobreavaliada. "
            report += "Recomendamos a venda ou substituição por ativos mais atrativos."
        else:
            report += f"{symbol} apresenta um equilíbrio entre pontos fortes e fracos. "
            report += "Recomendamos análise mais aprofundada antes de tomar decisões."
        
        return report

# Função principal para teste
def main():
    analyzer = StockAnalyzer()
    
    # Atualizar carteira
    portfolio = analyzer.update_portfolio()
    
    # Exibir ações da carteira
    print("Carteira da Clearview Capital:")
    for stock in portfolio['stocks']:
        print(f"{stock['symbol']} - {stock['name']} - {stock['evaluation']['rating']}")
    
    # Exibir favoritas
    favorites = analyzer.get_favorites()
    print("\nFavoritas da Clearview:")
    for stock in favorites:
        print(f"{stock['symbol']} - {stock['name']} - Potencial: {stock['graham_value']['potential']:.2f}%")
    
    # Gerar relatório para a primeira ação
    if portfolio['stocks']:
        report = analyzer.generate_report(portfolio['stocks'][0])
        print(f"\nRelatório de exemplo:\n{report}")

if __name__ == "__main__":
    main()
