// Funções para exportação de dados para Excel

// Classe para gerenciar os dados de usuários
class UserDataManager {
  constructor() {
    this.users = [];
    this.loadFromLocalStorage();
  }
  
  // Carregar dados do localStorage
  loadFromLocalStorage() {
    const storedData = localStorage.getItem('clearviewUserData');
    if (storedData) {
      try {
        this.users = JSON.parse(storedData);
      } catch (e) {
        console.error('Erro ao carregar dados de usuários:', e);
        this.users = [];
      }
    }
  }
  
  // Salvar dados no localStorage
  saveToLocalStorage() {
    localStorage.setItem('clearviewUserData', JSON.stringify(this.users));
  }
  
  // Adicionar novo usuário
  addUser(userData) {
    // Verificar se o usuário já existe
    const existingUserIndex = this.users.findIndex(user => user.email === userData.email);
    
    if (existingUserIndex >= 0) {
      // Atualizar usuário existente
      this.users[existingUserIndex] = {
        ...this.users[existingUserIndex],
        ...userData,
        lastUpdated: new Date().toISOString()
      };
    } else {
      // Adicionar novo usuário
      this.users.push({
        ...userData,
        id: this.generateUserId(),
        createdAt: new Date().toISOString(),
        lastUpdated: new Date().toISOString()
      });
    }
    
    // Salvar alterações
    this.saveToLocalStorage();
    
    // Enviar dados para o servidor (simulado)
    this.syncWithServer();
    
    return true;
  }
  
  // Gerar ID único para usuário
  generateUserId() {
    return 'user_' + Math.random().toString(36).substr(2, 9);
  }
  
  // Obter todos os usuários
  getAllUsers() {
    return this.users;
  }
  
  // Obter usuário por email
  getUserByEmail(email) {
    return this.users.find(user => user.email === email);
  }
  
  // Sincronizar dados com o servidor (simulado)
  syncWithServer() {
    console.log('Sincronizando dados com o servidor...', this.users);
    // Em uma implementação real, enviaríamos os dados para o servidor
    // fetch('/api/users/sync', {
    //   method: 'POST',
    //   headers: {
    //     'Content-Type': 'application/json',
    //   },
    //   body: JSON.stringify(this.users),
    // });
  }
  
  // Exportar dados para CSV
  exportToCSV() {
    if (this.users.length === 0) {
      return 'Sem dados para exportar';
    }
    
    // Obter cabeçalhos das colunas (todas as propriedades possíveis)
    const allKeys = new Set();
    this.users.forEach(user => {
      Object.keys(user).forEach(key => allKeys.add(key));
    });
    
    const headers = Array.from(allKeys);
    
    // Criar linha de cabeçalho
    let csv = headers.join(',') + '\n';
    
    // Adicionar dados de cada usuário
    this.users.forEach(user => {
      const row = headers.map(header => {
        const value = user[header] || '';
        // Escapar aspas e adicionar aspas ao redor de valores com vírgulas
        const escapedValue = String(value).replace(/"/g, '""');
        return `"${escapedValue}"`;
      });
      csv += row.join(',') + '\n';
    });
    
    return csv;
  }
  
  // Exportar dados para Excel (XLSX)
  exportToExcel() {
    // Em uma implementação real, usaríamos uma biblioteca como SheetJS
    // Por enquanto, vamos apenas exportar como CSV
    return this.exportToCSV();
  }
}

// Inicializar gerenciador de dados
const userDataManager = new UserDataManager();

// Função para registrar dados do usuário
function registerUserData(userData) {
  return userDataManager.addUser(userData);
}

// Função para exportar dados para Excel
function exportUserDataToExcel() {
  const csv = userDataManager.exportToCSV();
  
  // Criar blob com os dados CSV
  const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
  
  // Criar URL para o blob
  const url = URL.createObjectURL(blob);
  
  // Criar link para download
  const link = document.createElement('a');
  link.href = url;
  link.setAttribute('download', `clearview_users_${new Date().toISOString().split('T')[0]}.csv`);
  link.style.display = 'none';
  
  // Adicionar link ao documento
  document.body.appendChild(link);
  
  // Simular clique no link
  link.click();
  
  // Limpar
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
}

// Modificar a função saveUserDataToExport no auth.js para usar o gerenciador de dados
function saveUserDataToExport(userData) {
  registerUserData(userData);
}

// Adicionar função para criar botão de exportação no painel admin
function createExportButton() {
  const adminPanel = document.querySelector('.admin-panel');
  if (adminPanel) {
    const exportButton = document.createElement('button');
    exportButton.className = 'btn btn-primary';
    exportButton.textContent = 'Exportar Dados para Excel';
    exportButton.addEventListener('click', exportUserDataToExcel);
    
    adminPanel.appendChild(exportButton);
  }
}

// Inicializar quando o DOM estiver carregado
document.addEventListener('DOMContentLoaded', function() {
  // Verificar se há dados de usuário no localStorage
  const userData = localStorage.getItem('clearviewUser');
  if (userData) {
    try {
      const user = JSON.parse(userData);
      // Registrar dados do usuário no gerenciador
      registerUserData(user);
    } catch (e) {
      console.error('Erro ao processar dados do usuário:', e);
    }
  }
});
