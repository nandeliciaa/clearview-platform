#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
API REST para a Plataforma Inteligente da Clearview Capital.
Este módulo implementa os endpoints da API para comunicação entre
o frontend e o backend do sistema.
"""

import os
import sys
import json
from datetime import datetime
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS

# Adicionar diretório pai ao path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from analysis.stock_analyzer import StockAnalyzer
from analysis.graham_formula import calculate_brazilian_graham, calculate_graham_score

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("api_server.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("APIServer")

# Inicializar Flask app
app = Flask(__name__)
CORS(app)  # Habilitar CORS para todas as rotas

# Inicializar analisador de ações
data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
analyzer = StockAnalyzer(data_dir=data_dir)

@app.route('/api/health', methods=['GET'])
def health_check():
    """Endpoint para verificar se a API está funcionando."""
    return jsonify({
        'status': 'ok',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/stocks', methods=['GET'])
def get_stocks():
    """Endpoint para obter lista de ações monitoradas."""
    try:
        br_stocks = analyzer.br_stocks
        us_stocks = analyzer.us_stocks
        
        return jsonify({
            'status': 'success',
            'data': {
                'br_stocks': br_stocks,
                'us_stocks': us_stocks,
                'total': len(br_stocks) + len(us_stocks)
            }
        })
    except Exception as e:
        logger.error(f"Erro ao obter lista de ações: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/stock/<symbol>', methods=['GET'])
def get_stock(symbol):
    """Endpoint para obter dados de uma ação específica."""
    try:
        region = request.args.get('region', 'BR')
        
        # Verificar se já temos dados da ação
        stock_data = analyzer.stocks_data.get(symbol.upper(), {})
        
        # Se não temos dados ou eles estão desatualizados, buscar novos
        if not stock_data or 'last_update' not in stock_data:
            stock_data = analyzer.fetch_stock_data(symbol.upper(), region)
            analyzer.stocks_data[symbol.upper()] = stock_data
            analyzer.save_data()
        
        # Buscar fundamentals
        fundamentals = analyzer.fetch_fundamentals(symbol.upper(), region)
        
        # Calcular valor de Graham
        graham_value = analyzer.calculate_graham_value(symbol.upper(), fundamentals)
        
        # Avaliar ação
        evaluation = analyzer.evaluate_stock(symbol.upper(), fundamentals, graham_value)
        
        return jsonify({
            'status': 'success',
            'data': {
                'symbol': symbol.upper(),
                'name': stock_data.get('name', ''),
                'price': stock_data.get('price', 0),
                'change_1d': stock_data.get('change_1d', 0),
                'change_1y': stock_data.get('change_1y', 0),
                'currency': stock_data.get('currency', 'BRL'),
                'exchange': stock_data.get('exchange', ''),
                'fundamentals': fundamentals,
                'graham_value': graham_value,
                'evaluation': evaluation,
                'last_update': datetime.now().isoformat()
            }
        })
    except Exception as e:
        logger.error(f"Erro ao obter dados da ação {symbol}: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/portfolio', methods=['GET'])
def get_portfolio():
    """Endpoint para obter a carteira atual."""
    try:
        # Verificar se queremos forçar uma atualização
        force_update = request.args.get('force_update', 'false').lower() == 'true'
        
        if force_update:
            portfolio = analyzer.update_portfolio()
        else:
            # Tentar carregar a carteira do arquivo
            portfolio_file = os.path.join(data_dir, "portfolio.json")
            if os.path.exists(portfolio_file):
                with open(portfolio_file, 'r', encoding='utf-8') as f:
                    portfolio = json.load(f)
            else:
                # Se não existir, criar uma nova
                portfolio = analyzer.update_portfolio()
        
        return jsonify({
            'status': 'success',
            'data': portfolio
        })
    except Exception as e:
        logger.error(f"Erro ao obter carteira: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/favorites', methods=['GET'])
def get_favorites():
    """Endpoint para obter as ações favoritas."""
    try:
        favorites = analyzer.get_favorites()
        
        return jsonify({
            'status': 'success',
            'data': favorites
        })
    except Exception as e:
        logger.error(f"Erro ao obter favoritas: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/report/<symbol>', methods=['GET'])
def get_report(symbol):
    """Endpoint para gerar relatório de uma ação."""
    try:
        region = request.args.get('region', 'BR')
        
        # Buscar dados da ação
        stock_data = analyzer.fetch_stock_data(symbol.upper(), region)
        fundamentals = analyzer.fetch_fundamentals(symbol.upper(), region)
        graham_value = analyzer.calculate_graham_value(symbol.upper(), fundamentals)
        evaluation = analyzer.evaluate_stock(symbol.upper(), fundamentals, graham_value)
        
        # Montar objeto com todos os dados
        stock = {
            'symbol': symbol.upper(),
            'name': stock_data.get('name', ''),
            'price': stock_data.get('price', 0),
            'change_1d': stock_data.get('change_1d', 0),
            'fundamentals': fundamentals,
            'graham_value': graham_value,
            'evaluation': evaluation
        }
        
        # Gerar relatório
        report = analyzer.generate_report(stock)
        
        return jsonify({
            'status': 'success',
            'data': {
                'report': report,
                'stock': stock
            }
        })
    except Exception as e:
        logger.error(f"Erro ao gerar relatório para {symbol}: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/search', methods=['GET'])
def search_stocks():
    """Endpoint para pesquisar ações por código ou nome."""
    try:
        query = request.args.get('q', '').upper()
        
        if not query:
            return jsonify({
                'status': 'error',
                'message': 'Parâmetro de busca não fornecido'
            }), 400
        
        results = []
        
        # Normalizar a consulta (remover acentos)
        normalized_query = query.normalize("NFD").replace(/[\u0300-\u036f]/g, "")
        
        # Buscar correspondências em ações brasileiras
        for symbol in analyzer.br_stocks:
            # Verificar se já temos dados da ação
            stock_data = analyzer.stocks_data.get(symbol, {})
            
            if not stock_data:
                continue
            
            name = stock_data.get('name', '')
            long_name = stock_data.get('long_name', '')
            
            # Normalizar nomes
            normalized_name = name.upper().normalize("NFD").replace(/[\u0300-\u036f]/g, "")
            normalized_long_name = long_name.upper().normalize("NFD").replace(/[\u0300-\u036f]/g, "")
            
            # Verificar correspondências
            if (symbol.startswith(query) or 
                normalized_name.find(normalized_query) >= 0 or 
                normalized_long_name.find(normalized_query) >= 0):
                
                results.append({
                    'symbol': symbol,
                    'name': name,
                    'long_name': long_name,
                    'price': stock_data.get('price', 0),
                    'change': stock_data.get('change_1d', 0),
                    'region': 'BR'
                })
        
        # Buscar correspondências em ações americanas
        for symbol in analyzer.us_stocks:
            # Verificar se já temos dados da ação
            stock_data = analyzer.stocks_data.get(symbol, {})
            
            if not stock_data:
                continue
            
            name = stock_data.get('name', '')
            long_name = stock_data.get('long_name', '')
            
            # Normalizar nomes
            normalized_name = name.upper().normalize("NFD").replace(/[\u0300-\u036f]/g, "")
            normalized_long_name = long_name.upper().normalize("NFD").replace(/[\u0300-\u036f]/g, "")
            
            # Verificar correspondências
            if (symbol.startswith(query) or 
                normalized_name.find(normalized_query) >= 0 or 
                normalized_long_name.find(normalized_query) >= 0):
                
                results.append({
                    'symbol': symbol,
                    'name': name,
                    'long_name': long_name,
                    'price': stock_data.get('price', 0),
                    'change': stock_data.get('change_1d', 0),
                    'region': 'US'
                })
        
        return jsonify({
            'status': 'success',
            'data': {
                'query': query,
                'results': results,
                'count': len(results)
            }
        })
    except Exception as e:
        logger.error(f"Erro na pesquisa de ações: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/news', methods=['GET'])
def get_news():
    """Endpoint para obter notícias do mercado financeiro."""
    try:
        # Parâmetros opcionais
        symbol = request.args.get('symbol', None)
        limit = int(request.args.get('limit', 10))
        
        # Aqui seria implementada a busca de notícias
        # Por enquanto, vamos retornar notícias simuladas
        
        news = [
            {
                'title': 'Banco Central mantém taxa Selic em 10,5% ao ano',
                'date': '2025-04-21T18:00:00',
                'summary': 'O Comitê de Política Monetária (Copom) do Banco Central decidiu, por unanimidade, manter a taxa Selic em 10,5% ao ano, em linha com as expectativas do mercado.',
                'source': 'Banco Central',
                'url': 'https://www.bcb.gov.br/noticias',
                'related_stocks': ['BBAS3', 'ITUB4', 'BBDC4']
            },
            {
                'title': 'Inflação de março fica em 0,4%, abaixo das expectativas',
                'date': '2025-04-21T09:15:00',
                'summary': 'O IPCA de março ficou em 0,4%, abaixo da expectativa do mercado que era de 0,5%. No acumulado de 12 meses, a inflação está em 4,2%.',
                'source': 'IBGE',
                'url': 'https://www.ibge.gov.br/noticias',
                'related_stocks': []
            },
            {
                'title': 'Petrobras anuncia novo plano de investimentos',
                'date': '2025-04-20T10:30:00',
                'summary': 'A Petrobras anunciou hoje seu novo plano de investimentos para os próximos 5 anos, com foco em exploração e produção no pré-sal.',
                'source': 'InfoMoney',
                'url': 'https://www.infomoney.com.br/noticias',
                'related_stocks': ['PETR4', 'PETR3']
            },
            {
                'title': 'Fed sinaliza possível corte de juros nos EUA ainda este ano',
                'date': '2025-04-19T16:45:00',
                'summary': 'O Federal Reserve (Fed) sinalizou que pode reduzir as taxas de juros nos Estados Unidos ainda este ano, caso a inflação continue desacelerando.',
                'source': 'Bloomberg',
                'url': 'https://www.bloomberg.com/news',
                'related_stocks': ['AAPL', 'MSFT', 'GOOGL']
            },
            {
                'title': 'Vale reporta produção recorde de minério de ferro no primeiro trimestre',
                'date': '2025-04-18T09:00:00',
                'summary': 'A Vale reportou produção recorde de minério de ferro no primeiro trimestre de 2025, superando as expectativas do mercado e indicando forte demanda global.',
                'source': 'Valor Econômico',
                'url': 'https://www.valor.com.br/noticias',
                'related_stocks': ['VALE3']
            }
        ]
        
        # Filtrar por ação, se especificado
        if symbol:
            symbol = symbol.upper()
            filtered_news = []
            for item in news:
                if symbol in item['related_stocks'] or not item['related_stocks']:
                    filtered_news.append(item)
            news = filtered_news
        
        # Limitar quantidade
        news = news[:limit]
        
        return jsonify({
            'status': 'success',
            'data': {
                'news': news,
                'count': len(news),
                'last_update': datetime.now().isoformat()
            }
        })
    except Exception as e:
        logger.error(f"Erro ao obter notícias: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/market', methods=['GET'])
def get_market_data():
    """Endpoint para obter dados gerais do mercado."""
    try:
        # Aqui seria implementada a busca de dados do mercado
        # Por enquanto, vamos retornar dados simulados
        
        market_data = {
            'indices': {
                'IBOV': {
                    'name': 'Ibovespa',
                    'value': 125430.45,
                    'change': 1.2,
                    'last_update': datetime.now().isoformat()
                },
                'IFIX': {
                    'name': 'Índice de Fundos Imobiliários',
                    'value': 3245.67,
                    'change': 0.5,
                    'last_update': datetime.now().isoformat()
                },
                'SP500': {
                    'name': 'S&P 500',
                    'value': 5230.18,
                    'change': 0.8,
                    'last_update': datetime.now().isoformat()
                },
                'NASDAQ': {
                    'name': 'Nasdaq Composite',
                    'value': 16780.45,
                    'change': 1.1,
                    'last_update': datetime.now().isoformat()
                }
            },
            'currencies': {
                'USD/BRL': {
                    'name': 'Dólar/Real',
                    'value': 5.12,
                    'change': -0.3,
                    'last_update': datetime.now().isoformat()
                },
                'EUR/BRL': {
                    'name': 'Euro/Real',
                    'value': 5.58,
                    'change': -0.2,
                    'last_update': datetime.now().isoformat()
                },
                'BTC/USD': {
                    'name': 'Bitcoin/Dólar',
                    'value': 68450.25,
                    'change': 2.5,
                    'last_update': datetime.now().isoformat()
                }
            },
            'commodities': {
                'OIL': {
                    'name': 'Petróleo Brent',
                    'value': 82.45,
                    'change': 1.8,
                    'last_update': datetime.now().isoformat()
                },
                'GOLD': {
                    'name': 'Ouro',
                    'value': 2345.67,
                    'change': 0.7,
                    'last_update': datetime.now().isoformat()
                },
                'IRON': {
                    'name': 'Minério de Ferro',
                    'value': 120.34,
                    'change': -0.5,
                    'last_update': datetime.now().isoformat()
                }
            }
        }
        
        return jsonify({
            'status': 'success',
            'data': market_data
        })
    except Exception as e:
        logger.error(f"Erro ao obter dados do mercado: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/newsletter/subscribe', methods=['POST'])
def subscribe_newsletter():
    """Endpoint para cadastrar e-mail na newsletter."""
    try:
        data = request.json
        
        if not data or 'email' not in data:
            return jsonify({
                'status': 'error',
                'message': 'E-mail não fornecido'
            }), 400
        
        email = data['email']
        name = data.get('name', '')
        phone = data.get('phone', '')
        
        # Aqui seria implementado o cadastro do e-mail
        # Por enquanto, vamos apenas simular
        
        # Salvar em um arquivo JSON
        subscribers_file = os.path.join(data_dir, "newsletter_subscribers.json")
        
        subscribers = []
        if os.path.exists(subscribers_file):
            with open(subscribers_file, 'r', encoding='utf-8') as f:
                subscribers = json.load(f)
        
        # Verificar se o e-mail já está cadastrado
        for subscriber in subscribers:
            if subscriber['email'] == email:
                return jsonify({
                    'status': 'error',
                    'message': 'E-mail já cadastrado'
                }), 400
        
        # Adicionar novo assinante
        subscribers.append({
            'email': email,
            'name': name,
            'phone': phone,
            'date': datetime.now().isoformat()
        })
        
        # Salvar arquivo
        with open(subscribers_file, 'w', encoding='utf-8') as f:
            json.dump(subscribers, f, ensure_ascii=False, indent=2)
        
        return jsonify({
            'status': 'success',
            'message': 'Cadastro realizado com sucesso',
            'data': {
                'email': email,
                'name': name
            }
        })
    except Exception as e:
        logger.error(f"Erro ao cadastrar e-mail: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

def main():
    """Função principal para iniciar o servidor."""
    try:
        # Inicializar dados
        analyzer.update_portfolio()
        
        # Iniciar servidor
        app.run(host='0.0.0.0', port=5000, debug=True)
    except Exception as e:
        logger.error(f"Erro ao iniciar servidor: {e}")

if __name__ == "__main__":
    main()
