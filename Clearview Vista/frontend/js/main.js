// Funções para a Plataforma Inteligente da Clearview Capital

// Variáveis globais
let stockData = {};
let chartInstance = null;

// Inicialização quando o DOM estiver carregado
document.addEventListener('DOMContentLoaded', function() {
    // Inicializar tabs nos detalhes da ação
    initTabs();
    
    // Inicializar barra de pesquisa
    initSearchBar();
    
    // Inicializar gráfico de exemplo
    initStockChart();
    
    // Inicializar tabelas de ações expansíveis
    initExpandableRows();
    
    // Inicializar menu mobile
    initMobileMenu();
});

// Inicializar as tabs nos detalhes da ação
function initTabs() {
    const tabs = document.querySelectorAll('.stock-details-tab');
    const contents = document.querySelectorAll('.stock-details-content');
    
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            // Remover classe active de todas as tabs e conteúdos
            tabs.forEach(t => t.classList.remove('active'));
            contents.forEach(c => c.classList.remove('active'));
            
            // Adicionar classe active na tab clicada
            tab.classList.add('active');
            
            // Mostrar o conteúdo correspondente
            const tabId = tab.getAttribute('data-tab');
            document.getElementById(tabId + 'Tab').classList.add('active');
        });
    });
}

// Inicializar o menu mobile
function initMobileMenu() {
    const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
    const navContainer = document.querySelector('.nav-container');
    const userActions = document.querySelector('.user-actions');
    
    if (mobileMenuToggle) {
        mobileMenuToggle.addEventListener('click', () => {
            mobileMenuToggle.classList.toggle('active');
            navContainer.classList.toggle('active');
            userActions.classList.toggle('active');
        });
        
        // Fechar menu ao clicar em um link
        const navLinks = document.querySelectorAll('.nav-link');
        navLinks.forEach(link => {
            link.addEventListener('click', () => {
                mobileMenuToggle.classList.remove('active');
                navContainer.classList.remove('active');
                userActions.classList.remove('active');
            });
        });
    }
}

// Inicializar a barra de pesquisa
function initSearchBar() {
    const searchInput = document.querySelector('.search-input');
    const searchBtn = document.querySelector('.search-btn');
    const searchResults = document.getElementById('searchResults');
    const stockDetailsPanel = document.getElementById('stockDetailsPanel');
    
    // Evento de clique no botão de pesquisa
    searchBtn.addEventListener('click', () => {
        const query = searchInput.value.trim().toUpperCase();
        if (query) {
            searchStock(query);
        }
    });
    
    // Evento de tecla Enter no input de pesquisa
    searchInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            const query = searchInput.value.trim().toUpperCase();
            if (query) {
                searchStock(query);
            }
        }
    });
    
    // Evento de foco no input de pesquisa
    searchInput.addEventListener('focus', () => {
        // Mostrar resultados recentes ou sugestões
        searchResults.classList.add('active');
    });
    
    // Fechar resultados ao clicar fora
    document.addEventListener('click', (e) => {
        if (!searchInput.contains(e.target) && !searchResults.contains(e.target) && !searchBtn.contains(e.target)) {
            searchResults.classList.remove('active');
        }
    });
}

// Função para pesquisar ação
function searchStock(query) {
    // Aqui seria feita a chamada à API para obter dados da ação
    // Por enquanto, vamos simular com dados estáticos
    
    // Mostrar loader
    document.getElementById('searchResults').innerHTML = '<div class="loader"></div>';
    document.getElementById('searchResults').classList.add('active');
    
    // Simular delay de API
    setTimeout(() => {
        // Dados simulados
        const mockStocks = {
            'PETR4': {
                name: 'PETROBRAS PN',
                price: 'R$ 36,75',
                change: '+2,15%',
                pl: '6,8',
                pvp: '1,2',
                roe: '18,5%',
                dividendYield: '12,4%',
                debtToEbitda: '1,8',
                fairValue: 'R$ 42,30',
                potential: '+15,1%',
                rating: 'Compra'
            },
            'VALE3': {
                name: 'VALE ON',
                price: 'R$ 68,20',
                change: '+1,50%',
                pl: '5,2',
                pvp: '0,9',
                roe: '22,3%',
                dividendYield: '10,8%',
                debtToEbitda: '0,7',
                fairValue: 'R$ 75,40',
                potential: '+10,6%',
                rating: 'Compra'
            },
            'ITUB4': {
                name: 'ITAÚ UNIBANCO PN',
                price: 'R$ 34,85',
                change: '-0,35%',
                pl: '9,1',
                pvp: '2,3',
                roe: '20,1%',
                dividendYield: '5,2%',
                debtToEbitda: 'N/A',
                fairValue: 'R$ 38,20',
                potential: '+9,6%',
                rating: 'Manter'
            },
            'BBDC4': {
                name: 'BRADESCO PN',
                price: 'R$ 18,45',
                change: '-1,20%',
                pl: '8,3',
                pvp: '1,8',
                roe: '15,7%',
                dividendYield: '7,5%',
                debtToEbitda: 'N/A',
                fairValue: 'R$ 17,90',
                potential: '-3,0%',
                rating: 'Venda'
            },
            'WEGE3': {
                name: 'WEG ON',
                price: 'R$ 42,30',
                change: '+0,75%',
                pl: '28,5',
                pvp: '6,2',
                roe: '25,8%',
                dividendYield: '1,2%',
                debtToEbitda: '0,1',
                fairValue: 'R$ 38,50',
                potential: '-9,0%',
                rating: 'Manter'
            },
            'AAPL': {
                name: 'APPLE INC',
                price: 'US$ 169,30',
                change: '+0,85%',
                pl: '27,8',
                pvp: '32,5',
                roe: '145,2%',
                dividendYield: '0,5%',
                debtToEbitda: '1,1',
                fairValue: 'US$ 185,20',
                potential: '+9,4%',
                rating: 'Compra'
            }
        };
        
        // Mapeamento de nomes de empresas para códigos de ações
        const companyNameToSymbol = {
            'PETROBRAS': 'PETR4',
            'PETROLEO BRASILEIRO': 'PETR4',
            'VALE': 'VALE3',
            'ITAU': 'ITUB4',
            'ITAÚ': 'ITUB4',
            'ITAU UNIBANCO': 'ITUB4',
            'ITAÚ UNIBANCO': 'ITUB4',
            'BRADESCO': 'BBDC4',
            'WEG': 'WEGE3',
            'APPLE': 'AAPL'
        };
        
        // Normalizar a consulta (remover acentos, converter para maiúsculas)
        const normalizedQuery = query.toUpperCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "");
        
        // Verificar se a consulta é um código de ação
        if (mockStocks[normalizedQuery]) {
            displayStockResult(normalizedQuery, mockStocks[normalizedQuery]);
        } 
        // Verificar se a consulta é um nome de empresa
        else {
            let found = false;
            
            // Procurar correspondências parciais em nomes de empresas
            for (const [companyName, symbol] of Object.entries(companyNameToSymbol)) {
                const normalizedCompanyName = companyName.normalize("NFD").replace(/[\u0300-\u036f]/g, "");
                
                if (normalizedCompanyName.includes(normalizedQuery) || normalizedQuery.includes(normalizedCompanyName)) {
                    displayStockResult(symbol, mockStocks[symbol]);
                    found = true;
                    break;
                }
            }
            
            // Verificar correspondências parciais em códigos de ações
            if (!found) {
                for (const symbol in mockStocks) {
                    if (symbol.includes(normalizedQuery)) {
                        displayStockResult(symbol, mockStocks[symbol]);
                        found = true;
                        break;
                    }
                }
            }
            
            // Verificar correspondências parciais em nomes completos das ações
            if (!found) {
                for (const [symbol, data] of Object.entries(mockStocks)) {
                    const normalizedStockName = data.name.toUpperCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "");
                    
                    if (normalizedStockName.includes(normalizedQuery)) {
                        displayStockResult(symbol, data);
                        found = true;
                        break;
                    }
                }
            }
            
            // Se nenhuma correspondência for encontrada
            if (!found) {
                document.getElementById('searchResults').innerHTML = `
                    <div class="search-result-item">
                        Nenhum resultado encontrado para "${query}".
                    </div>
                `;
                
                // Esconder painel de detalhes
                document.getElementById('stockDetailsPanel').classList.remove('active');
            }
        }
    }, 1000);
}

// Função auxiliar para exibir os resultados da pesquisa
function displayStockResult(symbol, data) {
    stockData = data;
    
    // Atualizar resultados da pesquisa
    document.getElementById('searchResults').innerHTML = `
        <div class="search-result-item stock-search-result">
            <div class="stock-info">
                <span class="stock-symbol">${symbol}</span>
                <span class="stock-name">${stockData.name}</span>
            </div>
            <div>
                <span class="stock-price">${stockData.price}</span>
                <span class="stock-change ${stockData.change.includes('+') ? 'trend-up' : 'trend-down'}">${stockData.change}</span>
            </div>
        </div>
    `;
    
    // Atualizar painel de detalhes
    updateStockDetailsPanel(symbol, stockData);
    
    // Mostrar painel de detalhes
    document.getElementById('stockDetailsPanel').classList.add('active');
    
    // Atualizar gráfico
    updateStockChart(symbol);
}

// Função para atualizar o painel de detalhes da ação
function updateStockDetailsPanel(symbol, data) {
    // Atualizar cabeçalho
    document.getElementById('stockSymbol').textContent = symbol;
    document.getElementById('stockName').textContent = data.name;
    document.getElementById('stockPrice').textContent = data.price;
    
    const stockChangeElement = document.getElementById('stockChange');
    stockChangeElement.textContent = data.change;
    if (data.change.includes('+')) {
        stockChangeElement.classList.remove('trend-down');
        stockChangeElement.classList.add('trend-up');
    } else {
        stockChangeElement.classList.remove('trend-up');
        stockChangeElement.classList.add('trend-down');
    }
    
    // Atualizar indicadores
    document.getElementById('peRatio').textContent = data.pl;
    document.getElementById('pbRatio').textContent = data.pvp;
    document.getElementById('roe').textContent = data.roe;
    document.getElementById('dividendYield').textContent = data.dividendYield;
    document.getElementById('debtToEbitda').textContent = data.debtToEbitda;
    document.getElementById('fairValue').textContent = data.fairValue;
    
    const potentialElement = document.getElementById('potential');
    potentialElement.textContent = data.potential;
    if (data.potential.includes('+')) {
        potentialElement.classList.remove('trend-down');
        potentialElement.classList.add('trend-up');
    } else {
        potentialElement.classList.remove('trend-up');
        potentialElement.classList.add('trend-down');
    }
    
    // Atualizar avaliação da Clearview Capital (antes era IA)
    const ratingElement = document.getElementById('aiRating');
    ratingElement.innerHTML = '';
    
    let badgeClass = '';
    switch(data.rating) {
        case 'Compra':
            badgeClass = 'badge-success';
            break;
        case 'Manter':
            badgeClass = 'badge-warning';
            break;
        case 'Venda':
            badgeClass = 'badge-danger';
            break;
    }
    
    ratingElement.innerHTML = `<span class="badge ${badgeClass}">${data.rating}</span>`;
}

// Inicializar gráfico de exemplo
function initStockChart() {
    const ctx = document.getElementById('stockChart').getContext('2d');
    
    // Dados simulados para o gráfico
    const labels = [];
    const data = [];
    
    // Gerar dados para os últimos 30 dias
    const today = new Date();
    for (let i = 30; i >= 0; i--) {
        const date = new Date();
        date.setDate(today.getDate() - i);
        labels.push(date.toLocaleDateString('pt-BR'));
        
        // Gerar preço aleatório entre 30 e 40
        data.push(30 + Math.random() * 10);
    }
    
    // Criar gráfico
    chartInstance = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Preço (R$)',
                data: data,
                borderColor: '#FFD700',
                backgroundColor: 'rgba(255, 215, 0, 0.1)',
                borderWidth: 2,
                pointRadius: 0,
                pointHoverRadius: 5,
                pointHoverBackgroundColor: '#FFD700',
                pointHoverBorderColor: '#fff',
                pointHoverBorderWidth: 2,
                tension: 0.1,
                fill: true
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    mode: 'index',
                    intersect: false,
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    titleColor: '#fff',
                    bodyColor: '#fff',
                    borderColor: '#FFD700',
                    borderWidth: 1,
                    displayColors: false,
                    callbacks: {
                        label: function(context) {
                            return `R$ ${context.parsed.y.toFixed(2)}`;
                        }
                    }
                }
            },
            scales: {
                x: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        maxRotation: 0,
                        autoSkip: true,
                        maxTicksLimit: 6
                    }
                },
                y: {
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    },
                    ticks: {
                        callback: function(value) {
                            return `R$ ${value.toFixed(2)}`;
                        }
                    }
                }
            },
            interaction: {
                mode: 'index',
                intersect: false
            }
        }
    });
}

// Atualizar gráfico com dados da ação
function updateStockChart(symbol) {
    // Aqui seria feita a chamada à API para obter dados históricos da ação
    // Por enquanto, vamos simular com dados aleatórios
    
    // Gerar dados para os últimos 30 dias
    const labels = [];
    const data = [];
    
    const today = new Date();
    let basePrice = 0;
    
    // Definir preço base de acordo com o símbolo
    switch(symbol) {
        case 'PETR4':
            basePrice = 35;
            break;
        case 'VALE3':
            basePrice = 65;
            break;
        case 'ITUB4':
            basePrice = 32;
            break;
        case 'BBDC4':
            basePrice = 17;
            break;
        case 'WEGE3':
            basePrice = 40;
            break;
        case 'AAPL':
            basePrice = 165;
            break;
        default:
            basePrice = 30;
    }
    
    for (let i = 30; i >= 0; i--) {
        const date = new Date();
        date.setDate(today.getDate() - i);
        labels.push(date.toLocaleDateString('pt-BR'));
        
        // Gerar preço aleatório com variação de até 15%
        data.push(basePrice * (0.925 + Math.random() * 0.15));
    }
    
    // Atualizar dados do gráfico
    chartInstance.data.labels = labels;
    chartInstance.data.datasets[0].data = data;
    
    // Atualizar moeda no eixo Y se for ação internacional
    if (symbol === 'AAPL') {
        chartInstance.options.scales.y.ticks.callback = function(value) {
            return `US$ ${value.toFixed(2)}`;
        };
        chartInstance.options.plugins.tooltip.callbacks.label = function(context) {
            return `US$ ${context.parsed.y.toFixed(2)}`;
        };
    } else {
        chartInstance.options.scales.y.ticks.callback = function(value) {
            return `R$ ${value.toFixed(2)}`;
        };
        chartInstance.options.plugins.tooltip.callbacks.label = function(context) {
            return `R$ ${context.parsed.y.toFixed(2)}`;
        };
    }
    
    // Atualizar gráfico
    chartInstance.update();
}

// Inicializar tabelas de ações expansíveis
function initExpandableRows() {
    const stockRows = document.querySelectorAll('.stock-row');
    
    stockRows.forEach(row => {
        row.addEventListener('click', () => {
            row.classList.toggle('expanded');
        });
    });
}

// Função para atualizar cotações em tempo real
function updateRealTimeData() {
    // Aqui seria feita a chamada à API para obter dados atualizados
    // Por enquanto, vamos simular com pequenas variações aleatórias
    
    const stockRows = document.querySelectorAll('.stock-row');
    const dashboardCards = document.querySelectorAll('.card');
    
    // Atualizar data e hora
    const now = new Date();
    const formattedDate = now.toLocaleDateString('pt-BR');
    const formattedTime = now.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' });
    
    document.querySelectorAll('.section-header span').forEach(span => {
        if (span.textContent.includes('Atualizado')) {
            span.textContent = `Atualizado: ${formattedDate} - ${formattedTime}`;
        }
    });
    
    // Atualizar cotações nas tabelas
    stockRows.forEach(row => {
        const priceCell = row.querySelector('td:nth-child(3)');
        const changeCell = row.querySelector('td:nth-child(4)');
        
        if (priceCell && changeCell) {
            // Obter preço atual
            let currentPrice = parseFloat(priceCell.textContent.replace('R$ ', '').replace(',', '.'));
            
            // Gerar variação aleatória entre -0.5% e +0.5%
            const variation = currentPrice * (Math.random() * 0.01 - 0.005);
            const newPrice = currentPrice + variation;
            
            // Atualizar preço
            priceCell.textContent = `R$ ${newPrice.toFixed(2).replace('.', ',')}`;
            
            // Atualizar variação
            const percentChange = (variation / currentPrice) * 100;
            const sign = percentChange >= 0 ? '+' : '';
            changeCell.textContent = `${sign}${percentChange.toFixed(2).replace('.', ',')}%`;
            
            // Atualizar classe de tendência
            if (percentChange >= 0) {
                changeCell.classList.remove('trend-down');
                changeCell.classList.add('trend-up');
            } else {
                changeCell.classList.remove('trend-up');
                changeCell.classList.add('trend-down');
            }
        }
    });
    
    // Atualizar cards do dashboard
    dashboardCards.forEach(card => {
        const cardTitle = card.querySelector('.card-title');
        const cardValue = card.querySelector('.card-value');
        const cardTrend = card.querySelector('.card-footer .trend-up, .card-footer .trend-down');
        
        if (cardTitle && cardValue && cardTrend) {
            // Pular o card de oportunidades
            if (cardTitle.textContent === 'Oportunidades') {
                return;
            }
            
            // Obter valor atual
            let currentValue;
            let prefix = '';
            let suffix = '';
            
            if (cardTitle.textContent === 'Dólar') {
                prefix = 'R$ ';
                currentValue = parseFloat(cardValue.textContent.replace(prefix, '').replace(',', '.'));
            } else {
                currentValue = parseFloat(cardValue.textContent.replace('.', '').replace(',', '.'));
            }
            
            // Gerar variação aleatória entre -0.3% e +0.3%
            const variation = currentValue * (Math.random() * 0.006 - 0.003);
            const newValue = currentValue + variation;
            
            // Atualizar valor
            if (cardTitle.textContent === 'Dólar') {
                cardValue.textContent = `${prefix}${newValue.toFixed(2).replace('.', ',')}`;
            } else {
                cardValue.textContent = Math.round(newValue).toLocaleString('pt-BR');
            }
            
            // Atualizar variação
            const percentChange = (variation / currentValue) * 100;
            const sign = percentChange >= 0 ? '+' : '';
            cardTrend.textContent = `${sign}${percentChange.toFixed(1).replace('.', ',')}%`;
            
            // Atualizar classe de tendência
            if (percentChange >= 0) {
                cardTrend.classList.remove('trend-down');
                cardTrend.classList.add('trend-up');
            } else {
                cardTrend.classList.remove('trend-up');
                cardTrend.classList.add('trend-down');
            }
        }
    });
}

// Iniciar atualizações em tempo real
setInterval(updateRealTimeData, 5000); // Atualizar a cada 5 segundos

// Inicializar atualizações em tempo real imediatamente
document.addEventListener('DOMContentLoaded', function() {
    // Primeira atualização após 1 segundo
    setTimeout(updateRealTimeData, 1000);
});
