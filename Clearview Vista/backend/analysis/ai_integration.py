#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Módulo de integração com IA para a Plataforma Inteligente da Clearview Capital.
Este módulo implementa a análise de notícias, tradução de conteúdo internacional,
geração de relatórios em linguagem natural e tomada de decisões automatizadas.
"""

import os
import sys
import json
import logging
import requests
from datetime import datetime
import time
import re
import openai

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("ai_integration.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("AIIntegration")

class AIIntegration:
    """
    Classe para integração com modelos de IA para análise de notícias,
    tradução e geração de relatórios.
    """
    
    def __init__(self, data_dir="/home/ubuntu/clearview_project/data"):
        """
        Inicializa a integração com IA.
        
        Args:
            data_dir (str): Diretório para armazenamento de dados
        """
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
        
        # Configurar OpenAI (usando API gratuita conforme solicitado)
        # Em um ambiente de produção, a chave seria armazenada de forma segura
        # e não hardcoded no código
        self.use_openai = False
        try:
            # Verificar se temos uma chave de API configurada
            openai_key = os.environ.get("OPENAI_API_KEY", "")
            if openai_key:
                openai.api_key = openai_key
                self.use_openai = True
                logger.info("OpenAI API configurada com sucesso")
            else:
                logger.warning("Chave da API OpenAI não encontrada, usando alternativas")
        except Exception as e:
            logger.error(f"Erro ao configurar OpenAI: {e}")
        
        # Carregar dados salvos, se existirem
        self.news_data = self.load_news_data()
    
    def load_news_data(self):
        """Carrega dados de notícias salvas, se existirem."""
        try:
            news_file = os.path.join(self.data_dir, "news_data.json")
            if os.path.exists(news_file):
                with open(news_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {"news": [], "last_update": ""}
        except Exception as e:
            logger.error(f"Erro ao carregar dados de notícias: {e}")
            return {"news": [], "last_update": ""}
    
    def save_news_data(self):
        """Salva dados de notícias em arquivo JSON."""
        try:
            news_file = os.path.join(self.data_dir, "news_data.json")
            with open(news_file, 'w', encoding='utf-8') as f:
                json.dump(self.news_data, f, ensure_ascii=False, indent=2)
            logger.info(f"Dados de notícias salvos em {news_file}")
        except Exception as e:
            logger.error(f"Erro ao salvar dados de notícias: {e}")
    
    def fetch_financial_news(self, limit=20, language="pt-br"):
        """
        Busca notícias financeiras de diversas fontes.
        
        Args:
            limit (int): Número máximo de notícias a retornar
            language (str): Idioma das notícias (pt-br ou en-us)
            
        Returns:
            list: Lista de notícias
        """
        logger.info(f"Buscando notícias financeiras em {language}")
        
        # Em uma implementação real, buscaríamos notícias de APIs como:
        # - Alpha Vantage News API
        # - Yahoo Finance API
        # - Google News API
        # - Bloomberg API
        # - Reuters API
        
        # Para este exemplo, vamos simular notícias
        
        # Notícias em português
        br_news = [
            {
                'title': 'Banco Central mantém taxa Selic em 10,5% ao ano',
                'date': datetime.now().isoformat(),
                'summary': 'O Comitê de Política Monetária (Copom) do Banco Central decidiu, por unanimidade, manter a taxa Selic em 10,5% ao ano, em linha com as expectativas do mercado.',
                'source': 'Banco Central',
                'url': 'https://www.bcb.gov.br/noticias',
                'language': 'pt-br',
                'related_stocks': ['BBAS3', 'ITUB4', 'BBDC4'],
                'sentiment': None,
                'relevance': None
            },
            {
                'title': 'Inflação de março fica em 0,4%, abaixo das expectativas',
                'date': datetime.now().isoformat(),
                'summary': 'O IPCA de março ficou em 0,4%, abaixo da expectativa do mercado que era de 0,5%. No acumulado de 12 meses, a inflação está em 4,2%.',
                'source': 'IBGE',
                'url': 'https://www.ibge.gov.br/noticias',
                'language': 'pt-br',
                'related_stocks': [],
                'sentiment': None,
                'relevance': None
            },
            {
                'title': 'Petrobras anuncia novo plano de investimentos',
                'date': datetime.now().isoformat(),
                'summary': 'A Petrobras anunciou hoje seu novo plano de investimentos para os próximos 5 anos, com foco em exploração e produção no pré-sal.',
                'source': 'InfoMoney',
                'url': 'https://www.infomoney.com.br/noticias',
                'language': 'pt-br',
                'related_stocks': ['PETR4', 'PETR3'],
                'sentiment': None,
                'relevance': None
            },
            {
                'title': 'Vale reporta produção recorde de minério de ferro no primeiro trimestre',
                'date': datetime.now().isoformat(),
                'summary': 'A Vale reportou produção recorde de minério de ferro no primeiro trimestre de 2025, superando as expectativas do mercado e indicando forte demanda global.',
                'source': 'Valor Econômico',
                'url': 'https://www.valor.com.br/noticias',
                'language': 'pt-br',
                'related_stocks': ['VALE3'],
                'sentiment': None,
                'relevance': None
            },
            {
                'title': 'WEG supera expectativas e reporta lucro 15% maior no trimestre',
                'date': datetime.now().isoformat(),
                'summary': 'A WEG, fabricante de motores elétricos e equipamentos de automação, reportou lucro líquido 15% superior ao mesmo período do ano anterior, superando as expectativas dos analistas.',
                'source': 'Exame',
                'url': 'https://www.exame.com/noticias',
                'language': 'pt-br',
                'related_stocks': ['WEGE3'],
                'sentiment': None,
                'relevance': None
            }
        ]
        
        # Notícias em inglês
        us_news = [
            {
                'title': 'Fed signals potential interest rate cut later this year',
                'date': datetime.now().isoformat(),
                'summary': 'The Federal Reserve signaled it could reduce interest rates in the United States later this year if inflation continues to slow down.',
                'source': 'Bloomberg',
                'url': 'https://www.bloomberg.com/news',
                'language': 'en-us',
                'related_stocks': ['AAPL', 'MSFT', 'GOOGL'],
                'sentiment': None,
                'relevance': None
            },
            {
                'title': 'Apple unveils new AI features for iPhone and Mac',
                'date': datetime.now().isoformat(),
                'summary': 'Apple announced a suite of new AI features for its iPhone and Mac products, leveraging large language models to enhance user experience across its ecosystem.',
                'source': 'TechCrunch',
                'url': 'https://www.techcrunch.com/news',
                'language': 'en-us',
                'related_stocks': ['AAPL'],
                'sentiment': None,
                'relevance': None
            },
            {
                'title': 'Tesla delivers record number of vehicles in Q1',
                'date': datetime.now().isoformat(),
                'summary': 'Tesla delivered a record number of electric vehicles in the first quarter of 2025, beating analyst expectations despite increasing competition in the EV market.',
                'source': 'Reuters',
                'url': 'https://www.reuters.com/news',
                'language': 'en-us',
                'related_stocks': ['TSLA'],
                'sentiment': None,
                'relevance': None
            },
            {
                'title': 'Amazon expands same-day delivery to more cities',
                'date': datetime.now().isoformat(),
                'summary': 'Amazon announced the expansion of its same-day delivery service to 15 additional cities, increasing its competitive edge in the e-commerce space.',
                'source': 'CNBC',
                'url': 'https://www.cnbc.com/news',
                'language': 'en-us',
                'related_stocks': ['AMZN'],
                'sentiment': None,
                'relevance': None
            },
            {
                'title': 'Microsoft's cloud revenue surges 30% in latest quarter',
                'date': datetime.now().isoformat(),
                'summary': 'Microsoft reported a 30% increase in cloud revenue for its Azure platform, highlighting the continued strong demand for cloud computing services.',
                'source': 'Wall Street Journal',
                'url': 'https://www.wsj.com/news',
                'language': 'en-us',
                'related_stocks': ['MSFT'],
                'sentiment': None,
                'relevance': None
            }
        ]
        
        # Selecionar notícias com base no idioma
        if language == "pt-br":
            news = br_news
        elif language == "en-us":
            news = us_news
        else:
            # Se o idioma não for especificado, retornar todas as notícias
            news = br_news + us_news
        
        # Limitar quantidade
        news = news[:limit]
        
        # Atualizar dados de notícias
        self.news_data["news"] = news
        self.news_data["last_update"] = datetime.now().isoformat()
        self.save_news_data()
        
        return news
    
    def analyze_news_sentiment(self, news):
        """
        Analisa o sentimento de uma notícia usando IA.
        
        Args:
            news (dict): Notícia a ser analisada
            
        Returns:
            dict: Notícia com análise de sentimento
        """
        logger.info(f"Analisando sentimento da notícia: {news['title']}")
        
        # Se temos acesso à API OpenAI, usar para análise de sentimento
        if self.use_openai:
            try:
                # Preparar prompt para análise de sentimento
                prompt = f"""
                Analise o sentimento da seguinte notícia financeira:
                
                Título: {news['title']}
                Resumo: {news['summary']}
                Fonte: {news['source']}
                
                Classifique o sentimento como:
                - Positivo: se a notícia indica perspectivas positivas para o mercado ou ações relacionadas
                - Neutro: se a notícia é factual sem indicar direção clara
                - Negativo: se a notícia indica perspectivas negativas para o mercado ou ações relacionadas
                
                Também avalie a relevância da notícia para investidores em uma escala de 1 a 10.
                
                Responda apenas com um JSON no formato:
                {{
                    "sentiment": "positivo|neutro|negativo",
                    "relevance": número de 1 a 10,
                    "explanation": "breve explicação da análise"
                }}
                """
                
                # Fazer chamada à API
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "Você é um analista financeiro especializado em análise de notícias do mercado."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3,
                    max_tokens=150
                )
                
                # Extrair resposta
                result_text = response.choices[0].message.content.strip()
                
                # Extrair JSON da resposta
                json_match = re.search(r'{.*}', result_text, re.DOTALL)
                if json_match:
                    result = json.loads(json_match.group(0))
                    
                    # Atualizar notícia com análise
                    news['sentiment'] = result.get('sentiment', 'neutro')
                    news['relevance'] = result.get('relevance', 5)
                    news['sentiment_explanation'] = result.get('explanation', '')
                    
                    logger.info(f"Análise de sentimento concluída: {news['sentiment']}, relevância: {news['relevance']}")
                else:
                    # Fallback se não conseguir extrair JSON
                    logger.warning("Não foi possível extrair JSON da resposta da API")
                    news['sentiment'] = 'neutro'
                    news['relevance'] = 5
            except Exception as e:
                logger.error(f"Erro na análise de sentimento com OpenAI: {e}")
                # Fallback para análise simples
                news = self._simple_sentiment_analysis(news)
        else:
            # Fallback para análise simples se não temos acesso à API
            news = self._simple_sentiment_analysis(news)
        
        return news
    
    def _simple_sentiment_analysis(self, news):
        """
        Análise de sentimento simples baseada em palavras-chave.
        
        Args:
            news (dict): Notícia a ser analisada
            
        Returns:
            dict: Notícia com análise de sentimento
        """
        # Palavras-chave positivas
        positive_words = [
            'aumento', 'crescimento', 'lucro', 'recorde', 'supera', 'alta',
            'positivo', 'expansão', 'valorização', 'sucesso', 'melhora',
            'increase', 'growth', 'profit', 'record', 'exceeds', 'rise',
            'positive', 'expansion', 'appreciation', 'success', 'improvement'
        ]
        
        # Palavras-chave negativas
        negative_words = [
            'queda', 'redução', 'prejuízo', 'abaixo', 'crise', 'baixa',
            'negativo', 'contração', 'desvalorização', 'fracasso', 'piora',
            'decline', 'reduction', 'loss', 'below', 'crisis', 'fall',
            'negative', 'contraction', 'depreciation', 'failure', 'worsening'
        ]
        
        # Combinar título e resumo para análise
        text = (news['title'] + ' ' + news['summary']).lower()
        
        # Contar ocorrências de palavras positivas e negativas
        positive_count = sum(1 for word in positive_words if word.lower() in text)
        negative_count = sum(1 for word in negative_words if word.lower() in text)
        
        # Determinar sentimento
        if positive_count > negative_count:
            sentiment = 'positivo'
        elif negative_count > positive_count:
            sentiment = 'negativo'
        else:
            sentiment = 'neutro'
        
        # Determinar relevância (simples)
        # Notícias com mais palavras-chave (positivas ou negativas) são consideradas mais relevantes
        relevance = min(10, max(1, positive_count + negative_count))
        
        # Atualizar notícia
        news['sentiment'] = sentiment
        news['relevance'] = relevance
        
        return news
    
    def translate_news(self, news, target_language="pt-br"):
        """
        Traduz uma notícia para o idioma alvo.
        
        Args:
            news (dict): Notícia a ser traduzida
            target_language (str): Idioma alvo (pt-br ou en-us)
            
        Returns:
            dict: Notícia traduzida
        """
        # Se a notícia já está no idioma alvo, retornar sem alterações
        if news['language'] == target_language:
            return news
        
        logger.info(f"Traduzindo notícia de {news['language']} para {target_language}: {news['title']}")
        
        # Se temos acesso à API OpenAI, usar para tradução
        if self.use_openai:
            try:
                # Preparar prompt para tradução
                language_name = "português brasileiro" if target_language == "pt-br" else "inglês"
                prompt = f"""
                Traduza o seguinte texto para {language_name}:
                
                Título: {news['title']}
                Resumo: {news['summary']}
                
                Responda apenas com um JSON no formato:
                {{
                    "title": "título traduzido",
                    "summary": "resumo traduzido"
                }}
                """
                
                # Fazer chamada à API
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "Você é um tradutor profissional especializado em finanças e economia."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3,
                    max_tokens=300
                )
                
                # Extrair resposta
                result_text = response.choices[0].message.content.strip()
                
                # Extrair JSON da resposta
                json_match = re.search(r'{.*}', result_text, re.DOTALL)
                if json_match:
                    result = json.loads(json_match.group(0))
                    
                    # Criar cópia da notícia com tradução
                    translated_news = news.copy()
                    translated_news['title'] = result.get('title', news['title'])
                    translated_news['summary'] = result.get('summary', news['summary'])
                    translated_news['language'] = target_language
                    translated_news['original_language'] = news['language']
                    
                    logger.info(f"Tradução concluída: {translated_news['title']}")
                    
                    return translated_news
                else:
                    # Fallback se não conseguir extrair JSON
                    logger.warning("Não foi possível extrair JSON da resposta da API")
                    return news
            except Exception as e:
                logger.error(f"Erro na tradução com OpenAI: {e}")
                # Fallback para tradução simples
                return self._simple_translation(news, target_language)
        else:
            # Fallback para tradução simples se não temos acesso à API
            return self._simple_translation(news, target_language)
    
    def _simple_translation(self, news, target_language):
        """
        Tradução simples baseada em dicionário.
        
        Args:
            news (dict): Notícia a ser traduzida
            target_language (str): Idioma alvo (pt-br ou en-us)
            
        Returns:
            dict: Notícia com tradução simples
        """
        # Este é um método de fallback muito simples
        # Em uma implementação real, usaríamos uma API de tradução como Google Translate
        
        # Dicionário simples de tradução (apenas para demonstração)
        en_to_pt = {
            "Fed": "Fed",
            "interest rate": "taxa de juros",
            "cut": "corte",
            "Apple": "Apple",
            "AI": "IA",
            "features": "recursos",
            "iPhone": "iPhone",
            "Mac": "Mac",
            "Tesla": "Tesla",
            "delivers": "entrega",
            "record": "recorde",
            "vehicles": "veículos",
            "Amazon": "Amazon",
            "expands": "expande",
            "same-day delivery": "entrega no mesmo dia",
            "cities": "cidades",
            "Microsoft": "Microsoft",
            "cloud": "nuvem",
            "revenue": "receita",
            "surges": "aumenta",
            "quarter": "trimestre"
        }
        
        pt_to_en = {v: k for k, v in en_to_pt.items()}
        
        # Selecionar dicionário com base no idioma de origem e destino
        translation_dict = {}
        if news['language'] == "en-us" and target_language == "pt-br":
            translation_dict = en_to_pt
        elif news['language'] == "pt-br" and target_language == "en-us":
            translation_dict = pt_to_en
        
        # Criar cópia da notícia
        translated_news = news.copy()
        
        # Traduzir título e resumo (substituição simples de palavras)
        title = news['title']
        summary = news['summary']
        
        for source, target in translation_dict.items():
            title = title.replace(source, target)
            summary = summary.replace(source, target)
        
        translated_news['title'] = title
        translated_news['summary'] = summary
        translated_news['language'] = target_language
        translated_news['original_language'] = news['language']
        
        return translated_news
    
    def generate_stock_report(self, stock_data, fundamentals, evaluation):
        """
        Gera um relatório em linguagem natural para uma ação.
        
        Args:
            stock_data (dict): Dados da ação
            fundamentals (dict): Indicadores fundamentalistas
            evaluation (dict): Avaliação da ação
            
        Returns:
            str: Relatório em texto
        """
        logger.info(f"Gerando relatório para {stock_data.get('symbol', 'ação desconhecida')}")
        
        # Se temos acesso à API OpenAI, usar para geração de relatório
        if self.use_openai:
            try:
                # Preparar prompt para geração de relatório
                prompt = f"""
                Gere um relatório em linguagem natural para a seguinte ação:
                
                Símbolo: {stock_data.get('symbol', '')}
                Nome: {stock_data.get('name', '')}
                Preço: {stock_data.get('price', 0)}
                Variação: {stock_data.get('change_1d', 0)}%
                
                Indicadores Fundamentalistas:
                {json.dumps(fundamentals, indent=2)}
                
                Avaliação:
                {json.dumps(evaluation, indent=2)}
                
                O relatório deve ter linguagem leve, acessível e humana, como se fosse escrito por um analista da Clearview Capital.
                Deve explicar de forma clara os pontos fortes e fracos da ação, e justificar a recomendação (Compra, Manter ou Venda).
                Use linguagem em português brasileiro.
                """
                
                # Fazer chamada à API
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "Você é um analista financeiro da Clearview Capital, especializado em análise fundamentalista de ações."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=800
                )
                
                # Extrair resposta
                report = response.choices[0].message.content.strip()
                
                logger.info(f"Relatório gerado com sucesso: {len(report)} caracteres")
                
                return report
            except Exception as e:
                logger.error(f"Erro na geração de relatório com OpenAI: {e}")
                # Fallback para geração simples
                return self._generate_simple_report(stock_data, fundamentals, evaluation)
        else:
            # Fallback para geração simples se não temos acesso à API
            return self._generate_simple_report(stock_data, fundamentals, evaluation)
    
    def _generate_simple_report(self, stock_data, fundamentals, evaluation):
        """
        Gera um relatório simples para uma ação.
        
        Args:
            stock_data (dict): Dados da ação
            fundamentals (dict): Indicadores fundamentalistas
            evaluation (dict): Avaliação da ação
            
        Returns:
            str: Relatório em texto
        """
        symbol = stock_data.get('symbol', '')
        name = stock_data.get('name', '')
        price = stock_data.get('price', 0)
        change = stock_data.get('change_1d', 0)
        
        # Construir relatório
        report = f"Análise de {symbol} - {name}\n\n"
        
        # Resumo
        report += "Resumo:\n"
        report += f"Cotação atual: R$ {price:.2f} ({'+' if change >= 0 else ''}{change:.2f}%)\n"
        
        if 'graham_value' in stock_data:
            graham = stock_data['graham_value']
            report += f"Valor justo (Graham): R$ {graham.get('fair_value', 0):.2f}\n"
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
    
    def generate_market_summary(self, market_data, portfolio, news):
        """
        Gera um resumo do mercado para a newsletter diária.
        
        Args:
            market_data (dict): Dados do mercado
            portfolio (dict): Dados da carteira
            news (list): Lista de notícias
            
        Returns:
            str: Resumo do mercado em texto
        """
        logger.info("Gerando resumo do mercado para newsletter")
        
        # Se temos acesso à API OpenAI, usar para geração de resumo
        if self.use_openai:
            try:
                # Preparar prompt para geração de resumo
                prompt = f"""
                Gere um resumo do mercado financeiro para a newsletter diária da Clearview Capital.
                
                Dados do Mercado:
                {json.dumps(market_data, indent=2)}
                
                Carteira:
                {json.dumps(portfolio, indent=2)}
                
                Principais Notícias:
                {json.dumps(news[:5], indent=2)}
                
                O resumo deve ter linguagem leve, acessível e humana, como se fosse escrito por um analista da Clearview Capital.
                Deve incluir:
                1. Um resumo do dia no mercado (principais índices e movimentos)
                2. Destaques da carteira da Clearview Capital
                3. Principais notícias e seus impactos
                4. Perspectivas para o próximo pregão
                
                Use linguagem em português brasileiro.
                """
                
                # Fazer chamada à API
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "Você é um analista financeiro da Clearview Capital, especializado em análise de mercado e comunicação com investidores."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=1000
                )
                
                # Extrair resposta
                summary = response.choices[0].message.content.strip()
                
                logger.info(f"Resumo de mercado gerado com sucesso: {len(summary)} caracteres")
                
                return summary
            except Exception as e:
                logger.error(f"Erro na geração de resumo com OpenAI: {e}")
                # Fallback para geração simples
                return self._generate_simple_market_summary(market_data, portfolio, news)
        else:
            # Fallback para geração simples se não temos acesso à API
            return self._generate_simple_market_summary(market_data, portfolio, news)
    
    def _generate_simple_market_summary(self, market_data, portfolio, news):
        """
        Gera um resumo simples do mercado.
        
        Args:
            market_data (dict): Dados do mercado
            portfolio (dict): Dados da carteira
            news (list): Lista de notícias
            
        Returns:
            str: Resumo do mercado em texto
        """
        # Data atual
        today = datetime.now().strftime("%d/%m/%Y")
        
        # Construir resumo
        summary = f"Resumo do Mercado - {today}\n\n"
        
        # Índices
        summary += "Principais Índices:\n"
        for index_code, index_data in market_data.get('indices', {}).items():
            summary += f"- {index_data.get('name', index_code)}: {index_data.get('value', 0):.2f} "
            summary += f"({'+' if index_data.get('change', 0) >= 0 else ''}{index_data.get('change', 0):.2f}%)\n"
        summary += "\n"
        
        # Câmbio
        summary += "Câmbio:\n"
        for currency_code, currency_data in market_data.get('currencies', {}).items():
            summary += f"- {currency_data.get('name', currency_code)}: {currency_data.get('value', 0):.2f} "
            summary += f"({'+' if currency_data.get('change', 0) >= 0 else ''}{currency_data.get('change', 0):.2f}%)\n"
        summary += "\n"
        
        # Carteira
        summary += "Destaques da Carteira Clearview Capital:\n"
        
        # Ordenar ações da carteira por desempenho
        portfolio_stocks = sorted(
            portfolio.get('stocks', []),
            key=lambda x: x.get('change_1d', 0),
            reverse=True
        )
        
        # Mostrar as 3 melhores e as 3 piores
        best_stocks = portfolio_stocks[:3]
        worst_stocks = portfolio_stocks[-3:]
        
        summary += "Melhores desempenhos:\n"
        for stock in best_stocks:
            summary += f"- {stock.get('symbol', '')}: {stock.get('change_1d', 0):.2f}%\n"
        
        summary += "\nPiores desempenhos:\n"
        for stock in worst_stocks:
            summary += f"- {stock.get('symbol', '')}: {stock.get('change_1d', 0):.2f}%\n"
        
        summary += "\n"
        
        # Notícias
        summary += "Principais Notícias:\n"
        for i, news_item in enumerate(news[:5], 1):
            summary += f"{i}. {news_item.get('title', '')}\n"
            summary += f"   {news_item.get('summary', '')[:100]}...\n\n"
        
        # Perspectivas
        summary += "Perspectivas para o Próximo Pregão:\n"
        
        # Simular perspectiva com base no desempenho dos índices
        ibov_change = market_data.get('indices', {}).get('IBOV', {}).get('change', 0)
        sp500_change = market_data.get('indices', {}).get('SP500', {}).get('change', 0)
        
        if ibov_change > 1 and sp500_change > 0.5:
            summary += "O mercado apresenta tendência de alta, com bom desempenho tanto do Ibovespa quanto do S&P 500. "
            summary += "Esperamos continuidade do movimento positivo no próximo pregão, especialmente para ações de consumo e tecnologia."
        elif ibov_change < -1 and sp500_change < -0.5:
            summary += "O mercado apresenta tendência de baixa, com fraco desempenho tanto do Ibovespa quanto do S&P 500. "
            summary += "Recomendamos cautela no próximo pregão, com atenção especial para ações defensivas e dividendos."
        else:
            summary += "O mercado apresenta movimento lateral, sem tendência clara. "
            summary += "Para o próximo pregão, recomendamos seletividade nas operações, priorizando ações com bons fundamentos."
        
        return summary
    
    def send_telegram_notification(self, message, chat_id=None):
        """
        Envia notificação via Telegram.
        
        Args:
            message (str): Mensagem a ser enviada
            chat_id (str): ID do chat ou canal
            
        Returns:
            bool: True se enviado com sucesso, False caso contrário
        """
        logger.info("Enviando notificação via Telegram")
        
        # Em uma implementação real, usaríamos a API do Telegram
        # Para este exemplo, vamos apenas simular o envio
        
        # Verificar se temos um chat_id
        if not chat_id:
            chat_id = "@Clearview_Capital_Bot"  # Canal padrão
        
        # Simular envio
        logger.info(f"Notificação enviada para {chat_id}: {message[:50]}...")
        
        # Em uma implementação real, seria algo como:
        """
        bot_token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
        if not bot_token:
            logger.error("Token do bot Telegram não configurado")
            return False
        
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
        
        return True
    
    def send_email_newsletter(self, subject, content, recipients):
        """
        Envia newsletter por e-mail.
        
        Args:
            subject (str): Assunto do e-mail
            content (str): Conteúdo do e-mail (HTML)
            recipients (list): Lista de destinatários
            
        Returns:
            bool: True se enviado com sucesso, False caso contrário
        """
        logger.info(f"Enviando newsletter para {len(recipients)} destinatários")
        
        # Em uma implementação real, usaríamos um serviço de e-mail como SendGrid, Mailchimp, etc.
        # Para este exemplo, vamos apenas simular o envio
        
        # Simular envio
        logger.info(f"Newsletter enviada com assunto: {subject}")
        logger.info(f"Conteúdo: {content[:100]}...")
        logger.info(f"Destinatários: {recipients[:3]}...")
        
        # Em uma implementação real, seria algo como:
        """
        import smtplib
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        
        smtp_server = os.environ.get("SMTP_SERVER", "")
        smtp_port = int(os.environ.get("SMTP_PORT", "587"))
        smtp_user = os.environ.get("SMTP_USER", "")
        smtp_password = os.environ.get("SMTP_PASSWORD", "")
        
        if not all([smtp_server, smtp_port, smtp_user, smtp_password]):
            logger.error("Configurações de SMTP incompletas")
            return False
        
        try:
            # Configurar servidor SMTP
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(smtp_user, smtp_password)
            
            # Enviar e-mail para cada destinatário
            for recipient in recipients:
                # Criar mensagem
                msg = MIMEMultipart('alternative')
                msg['Subject'] = subject
                msg['From'] = f"Clearview Capital <{smtp_user}>"
                msg['To'] = recipient
                
                # Adicionar conteúdo HTML
                msg.attach(MIMEText(content, 'html'))
                
                # Enviar e-mail
                server.sendmail(smtp_user, recipient, msg.as_string())
            
            # Fechar conexão
            server.quit()
            
            logger.info(f"Newsletter enviada com sucesso para {len(recipients)} destinatários")
            return True
        except Exception as e:
            logger.error(f"Erro ao enviar newsletter: {e}")
            return False
        """
        
        return True
    
    def notify_opportunity(self, stock):
        """
        Notifica sobre uma nova oportunidade de investimento.
        
        Args:
            stock (dict): Dados da ação
            
        Returns:
            bool: True se notificado com sucesso, False caso contrário
        """
        logger.info(f"Notificando oportunidade: {stock.get('symbol', '')}")
        
        # Construir mensagem
        symbol = stock.get('symbol', '')
        name = stock.get('name', '')
        price = stock.get('price', 0)
        potential = stock.get('graham_value', {}).get('potential', 0)
        
        message = f"🔔 *OPORTUNIDADE CLEARVIEW* 🔔\n\n"
        message += f"*{symbol} - {name}*\n\n"
        message += f"Cotação atual: R$ {price:.2f}\n"
        message += f"Potencial de valorização: {potential:.2f}%\n\n"
        message += f"Esta ação está sendo negociada abaixo de 70% do seu valor justo!\n\n"
        message += f"Acesse a plataforma para mais detalhes."
        
        # Enviar notificação via Telegram
        telegram_success = self.send_telegram_notification(message)
        
        # Em uma implementação real, também enviaríamos notificações por outros canais
        
        return telegram_success
    
    def generate_daily_newsletter(self, market_data, portfolio, favorites, news):
        """
        Gera a newsletter diária.
        
        Args:
            market_data (dict): Dados do mercado
            portfolio (dict): Dados da carteira
            favorites (list): Lista de ações favoritas
            news (list): Lista de notícias
            
        Returns:
            dict: Newsletter gerada (assunto e conteúdo)
        """
        logger.info("Gerando newsletter diária")
        
        # Data atual
        today = datetime.now().strftime("%d/%m/%Y")
        
        # Gerar resumo do mercado
        market_summary = self.generate_market_summary(market_data, portfolio, news)
        
        # Construir assunto
        subject = f"Newsletter Clearview Capital - {today}"
        
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
                    max-width: 800px;
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
                h1, h2, h3 {{
                    color: #0047AB;
                }}
                .section {{
                    margin-bottom: 30px;
                    padding: 20px;
                    background-color: #f9f9f9;
                    border-radius: 5px;
                }}
                .stock-table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin-bottom: 20px;
                }}
                .stock-table th, .stock-table td {{
                    padding: 10px;
                    text-align: left;
                    border-bottom: 1px solid #ddd;
                }}
                .stock-table th {{
                    background-color: #0047AB;
                    color: white;
                }}
                .positive {{
                    color: green;
                }}
                .negative {{
                    color: red;
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
                <h1>Newsletter Diária</h1>
                <p>{today}</p>
            </div>
            
            <div class="section">
                <h2>Resumo do Mercado</h2>
                <p>{market_summary.replace('\n', '<br>')}</p>
            </div>
            
            <div class="section">
                <h2>Carteira da Clearview Capital</h2>
                <table class="stock-table">
                    <tr>
                        <th>Código</th>
                        <th>Empresa</th>
                        <th>Cotação</th>
                        <th>Variação</th>
                        <th>Avaliação</th>
                    </tr>
        """
        
        # Adicionar ações da carteira
        for stock in portfolio.get('stocks', [])[:10]:
            symbol = stock.get('symbol', '')
            name = stock.get('name', '')
            price = stock.get('price', 0)
            change = stock.get('change_1d', 0)
            rating = stock.get('evaluation', {}).get('rating', 'Neutro')
            
            change_class = "positive" if change >= 0 else "negative"
            change_sign = "+" if change >= 0 else ""
            
            content += f"""
                    <tr>
                        <td>{symbol}</td>
                        <td>{name}</td>
                        <td>R$ {price:.2f}</td>
                        <td class="{change_class}">{change_sign}{change:.2f}%</td>
                        <td>{rating}</td>
                    </tr>
            """
        
        content += """
                </table>
            </div>
            
            <div class="section">
                <h2>Favoritas da Clearview</h2>
                <table class="stock-table">
                    <tr>
                        <th>Código</th>
                        <th>Empresa</th>
                        <th>Cotação</th>
                        <th>Valor Justo</th>
                        <th>Potencial</th>
                    </tr>
        """
        
        # Adicionar ações favoritas
        for stock in favorites[:5]:
            symbol = stock.get('symbol', '')
            name = stock.get('name', '')
            price = stock.get('price', 0)
            fair_value = stock.get('graham_value', {}).get('fair_value', 0)
            potential = stock.get('graham_value', {}).get('potential', 0)
            
            potential_class = "positive" if potential >= 0 else "negative"
            potential_sign = "+" if potential >= 0 else ""
            
            content += f"""
                    <tr>
                        <td>{symbol}</td>
                        <td>{name}</td>
                        <td>R$ {price:.2f}</td>
                        <td>R$ {fair_value:.2f}</td>
                        <td class="{potential_class}">{potential_sign}{potential:.2f}%</td>
                    </tr>
            """
        
        content += """
                </table>
            </div>
            
            <div class="section">
                <h2>Notícias do Dia</h2>
        """
        
        # Adicionar notícias
        for news_item in news[:5]:
            title = news_item.get('title', '')
            summary = news_item.get('summary', '')
            source = news_item.get('source', '')
            url = news_item.get('url', '#')
            
            content += f"""
                <div>
                    <h3><a href="{url}">{title}</a></h3>
                    <p>{summary}</p>
                    <p><small>Fonte: {source}</small></p>
                </div>
                <hr>
            """
        
        content += """
            </div>
            
            <div class="footer">
                <p>© Clearview Capital. Todos os direitos reservados.</p>
                <p>Este e-mail foi enviado para você porque você se inscreveu em nossa newsletter.</p>
                <p>Para cancelar a inscrição, <a href="#">clique aqui</a>.</p>
            </div>
        </body>
        </html>
        """
        
        return {
            'subject': subject,
            'content': content
        }

# Função principal para teste
def main():
    ai = AIIntegration()
    
    # Buscar notícias
    news = ai.fetch_financial_news(limit=5)
    print(f"Notícias obtidas: {len(news)}")
    
    # Analisar sentimento da primeira notícia
    if news:
        analyzed_news = ai.analyze_news_sentiment(news[0])
        print(f"Sentimento: {analyzed_news.get('sentiment')}")
        print(f"Relevância: {analyzed_news.get('relevance')}")
    
    # Traduzir notícia em inglês para português
    en_news = {
        'title': 'Fed signals potential interest rate cut later this year',
        'summary': 'The Federal Reserve signaled it could reduce interest rates in the United States later this year if inflation continues to slow down.',
        'source': 'Bloomberg',
        'language': 'en-us'
    }
    
    translated_news = ai.translate_news(en_news, target_language="pt-br")
    print(f"Título traduzido: {translated_news.get('title')}")
    
    # Simular dados para geração de relatório
    stock_data = {
        'symbol': 'PETR4',
        'name': 'PETROBRAS PN',
        'price': 36.75,
        'change_1d': 2.15
    }
    
    fundamentals = {
        'P/L': 6.8,
        'P/VP': 1.2,
        'ROE': 18.5,
        'Dividend Yield': 12.4,
        'Dívida/EBITDA': 1.8
    }
    
    evaluation = {
        'rating': 'Compra',
        'strengths': [
            'P/L baixo, indicando possível subavaliação',
            'Dividend Yield atrativo',
            'Bom potencial segundo fórmula de Graham'
        ],
        'weaknesses': []
    }
    
    report = ai.generate_stock_report(stock_data, fundamentals, evaluation)
    print(f"Relatório gerado: {len(report)} caracteres")
    print(report[:200] + "...")
    
    # Simular notificação de oportunidade
    stock_data['graham_value'] = {'potential': 35.0}
    ai.notify_opportunity(stock_data)

if __name__ == "__main__":
    main()
