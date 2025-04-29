const express = require('express');
const serveStatic = require('serve-static');
const path = require('path');

// Criar aplicação Express
const app = express();

// Servir arquivos estáticos da pasta frontend
app.use('/', serveStatic(path.join(__dirname, 'frontend')));

// Para qualquer rota não encontrada, redirecionar para index.html
app.get('*', function(req, res) {
  res.sendFile(path.join(__dirname, 'frontend', 'index.html'));
});

// Obter porta do ambiente ou usar 8080 como padrão
const port = process.env.PORT || 8080;

// Iniciar servidor
app.listen(port, () => {
  console.log(`Servidor iniciado na porta ${port}`);
});
