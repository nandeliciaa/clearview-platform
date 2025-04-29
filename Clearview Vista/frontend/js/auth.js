// Funções para autenticação e gerenciamento de usuários

// Inicialização quando o DOM estiver carregado
document.addEventListener('DOMContentLoaded', function() {
    // Inicializar modais
    initModals();
    
    // Inicializar formulários
    initForms();
    
    // Inicializar chat
    initChat();
});

// Inicializar modais
function initModals() {
    // Botões para abrir modais
    const loginBtn = document.getElementById('loginBtn');
    const registerBtn = document.getElementById('registerBtn');
    
    // Verificar se os elementos existem antes de adicionar event listeners
    if (loginBtn) {
        loginBtn.addEventListener('click', function() {
            openModal('loginModal');
        });
    }
    
    if (registerBtn) {
        registerBtn.addEventListener('click', function() {
            openModal('registerModal');
        });
    }
    
    // Adicionar event listeners para links entre modais
    document.addEventListener('click', function(e) {
        // Link para mostrar modal de registro
        if (e.target && e.target.id === 'showRegisterModal') {
            e.preventDefault();
            closeModal('loginModal');
            setTimeout(() => {
                openModal('registerModal');
            }, 300);
        }
        
        // Link para mostrar modal de login
        if (e.target && e.target.id === 'showLoginModal') {
            e.preventDefault();
            closeModal('registerModal');
            setTimeout(() => {
                openModal('loginModal');
            }, 300);
        }
        
        // Botões para fechar modais
        if (e.target && e.target.classList.contains('close-modal')) {
            const modal = e.target.closest('.modal');
            if (modal) {
                closeModal(modal.id);
            }
        }
    });
    
    // Fechar modal ao clicar fora
    window.addEventListener('click', function(e) {
        if (e.target.classList.contains('modal')) {
            closeModal(e.target.id);
        }
    });
}

// Abrir modal
function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = 'block';
        document.body.style.overflow = 'hidden'; // Impedir rolagem da página
    }
}

// Fechar modal
function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = 'none';
        document.body.style.overflow = ''; // Restaurar rolagem da página
    }
}

// Inicializar formulários
function initForms() {
    // Formulário de login
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const email = document.getElementById('loginEmail').value;
            const password = document.getElementById('loginPassword').value;
            
            // Simulação de login
            loginUser(email, password);
        });
    }
    
    // Formulário de cadastro
    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
        registerForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const name = document.getElementById('registerName').value;
            const email = document.getElementById('registerEmail').value;
            const phone = document.getElementById('registerPhone').value;
            const password = document.getElementById('registerPassword').value;
            const passwordConfirm = document.getElementById('registerPasswordConfirm').value;
            const termsAccept = document.getElementById('termsAccept').checked;
            const newsletterAccept = document.getElementById('newsletterAccept').checked;
            
            // Validar senha
            if (password !== passwordConfirm) {
                alert('As senhas não coincidem. Por favor, tente novamente.');
                return;
            }
            
            // Validar aceitação dos termos
            if (!termsAccept) {
                alert('Você precisa aceitar os termos de uso e política de privacidade para continuar.');
                return;
            }
            
            // Simulação de cadastro
            registerUser(name, email, phone, password, newsletterAccept);
        });
    }
}

// Função para login de usuário
function loginUser(email, password) {
    // Aqui seria feita a chamada à API para autenticar o usuário
    // Por enquanto, vamos simular com um delay
    
    // Mostrar loader ou mensagem de carregamento
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.innerHTML = '<div class="loader"></div><p class="text-center">Autenticando...</p>';
    }
    
    // Simular delay de API
    setTimeout(() => {
        // Simular autenticação bem-sucedida
        // Em uma implementação real, verificaríamos a resposta da API
        
        // Salvar dados do usuário no localStorage
        const userData = {
            email: email,
            name: 'Usuário da Clearview',
            isLoggedIn: true,
            loginDate: new Date().toISOString()
        };
        
        localStorage.setItem('clearviewUser', JSON.stringify(userData));
        
        // Fechar modal
        closeModal('loginModal');
        
        // Atualizar UI para usuário logado
        updateUIForLoggedInUser(userData);
        
        // Registrar dados no sistema de exportação
        saveUserDataToExport(userData);
        
        // Exibir mensagem de sucesso
        alert('Login realizado com sucesso!');
        
        // Recarregar a página para atualizar o estado
        window.location.reload();
    }, 1500);
}

// Função para cadastro de usuário
function registerUser(name, email, phone, password, newsletter) {
    // Aqui seria feita a chamada à API para cadastrar o usuário
    // Por enquanto, vamos simular com um delay
    
    // Mostrar loader ou mensagem de carregamento
    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
        registerForm.innerHTML = '<div class="loader"></div><p class="text-center">Processando cadastro...</p>';
    }
    
    // Simular delay de API
    setTimeout(() => {
        // Simular cadastro bem-sucedido
        // Em uma implementação real, verificaríamos a resposta da API
        
        // Criar objeto com dados do usuário
        const userData = {
            name: name,
            email: email,
            phone: phone,
            newsletter: newsletter,
            registrationDate: new Date().toISOString(),
            isLoggedIn: true
        };
        
        // Salvar dados do usuário no localStorage
        localStorage.setItem('clearviewUser', JSON.stringify(userData));
        
        // Fechar modal
        closeModal('registerModal');
        
        // Atualizar UI para usuário logado
        updateUIForLoggedInUser(userData);
        
        // Registrar dados no sistema de exportação
        saveUserDataToExport(userData);
        
        // Exibir mensagem de sucesso
        alert('Cadastro realizado com sucesso! Bem-vindo à Clearview Capital.');
        
        // Recarregar a página para atualizar o estado
        window.location.reload();
    }, 2000);
}

// Atualizar UI para usuário logado
function updateUIForLoggedInUser(userData) {
    const userActions = document.querySelector('.user-actions');
    if (userActions) {
        userActions.innerHTML = `
            <div class="user-profile">
                <span class="user-name">Olá, ${userData.name.split(' ')[0]}</span>
                <button class="btn btn-outline btn-sm" id="logoutBtn">Sair</button>
            </div>
        `;
        
        // Adicionar event listener para botão de logout
        const logoutBtn = document.getElementById('logoutBtn');
        if (logoutBtn) {
            logoutBtn.addEventListener('click', logoutUser);
        }
    }
}

// Função para logout de usuário
function logoutUser() {
    // Remover dados do usuário do localStorage
    localStorage.removeItem('clearviewUser');
    
    // Recarregar a página para atualizar o estado
    window.location.reload();
}

// Verificar se o usuário está logado ao carregar a página
function checkUserLoginStatus() {
    const userData = localStorage.getItem('clearviewUser');
    if (userData) {
        const user = JSON.parse(userData);
        if (user.isLoggedIn) {
            updateUIForLoggedInUser(user);
        }
    }
}

// Registrar dados do usuário para exportação
function saveUserDataToExport(userData) {
    // Em uma implementação real, enviaríamos esses dados para o backend
    // para serem salvos em um banco de dados e posteriormente exportados para Excel
    
    console.log('Dados do usuário registrados para exportação:', userData);
    
    // Simular envio para o backend
    // fetch('/api/users', {
    //     method: 'POST',
    //     headers: {
    //         'Content-Type': 'application/json',
    //     },
    //     body: JSON.stringify(userData),
    // })
    // .then(response => response.json())
    // .then(data => {
    //     console.log('Sucesso:', data);
    // })
    // .catch((error) => {
    //     console.error('Erro:', error);
    // });
}

// Inicializar chat
function initChat() {
    const chatButton = document.querySelector('.chat-button');
    const chatWindow = document.querySelector('.chat-window');
    const chatClose = document.querySelector('.chat-close');
    const chatInput = document.querySelector('.chat-input');
    const chatSend = document.querySelector('.chat-send');
    const chatMessages = document.querySelector('.chat-messages');
    
    // Verificar se os elementos existem antes de adicionar event listeners
    if (chatButton && chatWindow) {
        // Abrir/fechar chat ao clicar no botão
        chatButton.addEventListener('click', function() {
            chatWindow.classList.toggle('active');
        });
        
        // Fechar chat ao clicar no X
        if (chatClose) {
            chatClose.addEventListener('click', function() {
                chatWindow.classList.remove('active');
            });
        }
        
        // Enviar mensagem ao clicar no botão ou pressionar Enter
        if (chatInput && chatSend && chatMessages) {
            // Enviar ao clicar no botão
            chatSend.addEventListener('click', function() {
                sendChatMessage();
            });
            
            // Enviar ao pressionar Enter
            chatInput.addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    sendChatMessage();
                }
            });
        }
    }
}

// Função para enviar mensagem no chat
function sendChatMessage() {
    const chatInput = document.querySelector('.chat-input');
    const chatMessages = document.querySelector('.chat-messages');
    
    if (chatInput && chatMessages) {
        const message = chatInput.value.trim();
        
        if (message) {
            // Adicionar mensagem do usuário
            chatMessages.innerHTML += `
                <div class="chat-message message-user">
                    ${message}
                </div>
            `;
            
            // Limpar input
            chatInput.value = '';
            
            // Rolar para o final das mensagens
            chatMessages.scrollTop = chatMessages.scrollHeight;
            
            // Mostrar indicador de digitação
            chatMessages.innerHTML += `
                <div class="typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
            `;
            
            // Rolar para o final das mensagens
            chatMessages.scrollTop = chatMessages.scrollHeight;
            
            // Simular resposta do assistente após um delay
            setTimeout(() => {
                // Remover indicador de digitação
                const typingIndicator = document.querySelector('.typing-indicator');
                if (typingIndicator) {
                    typingIndicator.remove();
                }
                
                // Gerar resposta com base na mensagem
                const response = generateChatResponse(message);
                
                // Adicionar resposta do assistente
                chatMessages.innerHTML += `
                    <div class="chat-message message-bot">
                        ${response}
                    </div>
                `;
                
                // Rolar para o final das mensagens
                chatMessages.scrollTop = chatMessages.scrollHeight;
            }, 1500);
        }
    }
}

// Função para gerar resposta do chat
function generateChatResponse(message) {
    // Converter mensagem para minúsculas para facilitar a comparação
    const lowerMessage = message.toLowerCase();
    
    // Respostas pré-definidas com base em palavras-chave
    if (lowerMessage.includes('olá') || lowerMessage.includes('oi') || lowerMessage.includes('bom dia') || lowerMessage.includes('boa tarde') || lowerMessage.includes('boa noite')) {
        return 'Olá! Como posso ajudar você hoje?';
    } else if (lowerMessage.includes('investir') || lowerMessage.includes('investimento')) {
        return 'A Clearview Capital oferece análises detalhadas para ajudar em suas decisões de investimento. Recomendamos verificar nossa carteira recomendada e as ações favoritas para começar.';
    } else if (lowerMessage.includes('ação') || lowerMessage.includes('ações') || lowerMessage.includes('bolsa')) {
        return 'Você pode pesquisar ações específicas usando a barra de pesquisa no topo da página. Também oferecemos análises detalhadas e recomendações em nossa seção de carteira.';
    } else if (lowerMessage.includes('cadastro') || lowerMessage.includes('cadastrar') || lowerMessage.includes('conta')) {
        return 'Para se cadastrar, clique no botão "Cadastrar" no topo da página. É rápido e gratuito!';
    } else if (lowerMessage.includes('newsletter') || lowerMessage.includes('email') || lowerMessage.includes('e-mail')) {
        return 'Nossa newsletter é enviada diariamente ao final do pregão com análises e recomendações. Para recebê-la, basta se cadastrar em nossa plataforma.';
    } else if (lowerMessage.includes('contato') || lowerMessage.includes('ajuda') || lowerMessage.includes('suporte')) {
        return 'Para entrar em contato com nossa equipe, envie um e-mail para contato@clearviewcapital.com.br ou use este chat para dúvidas rápidas.';
    } else if (lowerMessage.includes('obrigado') || lowerMessage.includes('obrigada') || lowerMessage.includes('valeu')) {
        return 'Por nada! Estou sempre à disposição para ajudar. Tem mais alguma dúvida?';
    } else {
        return 'Entendi sua mensagem. Para informações mais específicas sobre investimentos e análises de ações, recomendo explorar nossa plataforma ou entrar em contato com nossa equipe pelo e-mail contato@clearviewcapital.com.br';
    }
}

// Verificar status de login ao carregar a página
document.addEventListener('DOMContentLoaded', function() {
    checkUserLoginStatus();
});
