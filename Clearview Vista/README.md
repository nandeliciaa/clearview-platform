# Plataforma Inteligente da Clearview Capital

Uma plataforma de análise financeira com inteligência artificial para gestão automatizada de carteira de investimentos.

## Visão Geral

A Plataforma Inteligente da Clearview Capital é um sistema completo para análise de ações, identificação de oportunidades de investimento e gestão automatizada de carteira. Utilizando dados financeiros em tempo real e algoritmos de inteligência artificial, a plataforma identifica ações subavaliadas com base em critérios fundamentalistas e na fórmula de Graham.

## Funcionalidades Principais

- **Interface Intuitiva**: Design moderno e responsivo com esquema de cores preto, branco e cinza escuro com detalhes em azul
- **Barra de Pesquisa Avançada**: Busca de ações por código ou nome da empresa
- **Análise Fundamentalista**: Cálculo de indicadores como P/L, P/VP, ROE, Dividend Yield e Dívida/EBITDA
- **Fórmula de Graham**: Cálculo do valor justo das ações com adaptações para o mercado brasileiro
- **Integração com IA**: Análise de notícias, geração de relatórios e recomendações automatizadas
- **Sistema de Notificações**: Alertas por e-mail, Telegram, notificações push e na plataforma
- **Newsletter Diária**: Resumo do mercado, carteira recomendada e oportunidades identificadas

## Arquitetura do Sistema

A plataforma é dividida em quatro componentes principais:

1. **Frontend**: Interface web responsiva desenvolvida com HTML, CSS e JavaScript
2. **Sistema de Análise Financeira**: Módulos Python para coleta de dados e análise fundamentalista
3. **Integração com IA**: Análise de sentimento de notícias e geração de relatórios
4. **Sistema de Notificações**: Envio de alertas e newsletter por múltiplos canais

## Tecnologias Utilizadas

- **Frontend**: HTML5, CSS3, JavaScript
- **Backend**: Python, Flask
- **APIs de Dados**: Yahoo Finance
- **Inteligência Artificial**: ChatGPT para análise de notícias e geração de relatórios
- **Notificações**: E-mail, Telegram, Web Push

## Instalação e Execução

### Pré-requisitos

- Python 3.10+
- Pip (gerenciador de pacotes Python)
- Navegador web moderno

### Instalação

1. Clone o repositório:
   ```
   git clone https://github.com/clearview-capital/plataforma-inteligente.git
   cd plataforma-inteligente
   ```

2. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```

3. Configure as variáveis de ambiente (opcional):
   ```
   export OPENAI_API_KEY="sua_chave_api"
   export TELEGRAM_BOT_TOKEN="seu_token_bot"
   ```

### Execução

1. Inicie a plataforma:
   ```
   python run.py
   ```

2. Acesse a interface web:
   ```
   http://localhost:5000
   ```

## Estrutura de Diretórios

```
clearview_project/
├── frontend/               # Interface web
│   ├── css/                # Estilos CSS
│   ├── js/                 # Scripts JavaScript
│   ├── img/                # Imagens e recursos
│   └── index.html          # Página principal
├── backend/                # Servidor e API
│   ├── api_server.py       # Servidor Flask
│   ├── notification_system.py  # Sistema de notificações
│   └── analysis/           # Módulos de análise
│       ├── stock_analyzer.py   # Analisador de ações
│       ├── graham_formula.py   # Implementação da fórmula de Graham
│       └── ai_integration.py   # Integração com IA
├── data/                   # Armazenamento de dados
├── docs/                   # Documentação
└── run.py                  # Script principal
```

## Uso da Plataforma

1. **Pesquisa de Ações**: Use a barra de pesquisa para buscar ações por código (ex: PETR4) ou nome (ex: Petrobras)
2. **Análise de Ações**: Visualize indicadores fundamentalistas, valor justo e recomendações
3. **Carteira Recomendada**: Acesse a carteira automaticamente gerenciada pela plataforma
4. **Configuração de Alertas**: Defina alertas personalizados para preços e oportunidades
5. **Newsletter**: Inscreva-se para receber a newsletter diária com análises e recomendações

## Contribuição

Contribuições são bem-vindas! Para contribuir:

1. Faça um fork do repositório
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo LICENSE para detalhes.

## Contato

Clearview Capital - contato@clearview-capital.com

---

Desenvolvido por Clearview Capital © 2025
