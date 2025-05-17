// Definir palavras reservadas para o pseudocódigo
    const palavrasReservadas = [
      "Escrever", "Ler", "numero", "decimal", "texto", "Se", "Senao", "Enquanto", "FimSe", "FimEnquanto"
    ];

    // Registrar um simples modo para destacar palavras reservadas
    CodeMirror.defineSimpleMode("alexMode", {
      start: [
        {regex: /\/\/.*/, token: "comment"},
        {regex: /\/\*[\s\S]*?\*\//, token: "comment"},
        {regex: new RegExp("\\b(" + palavrasReservadas.join("|") + ")\\b", "i"), token: "keyword"},
        {regex: /\b\d+(\.\d+)?\b/, token: "number"},
        {regex: /"(?:[^\\]|\\.)*?"/, token: "string"},
        {regex: /'(?:[^\\]|\\.)*?'/, token: "string"},
        {regex: /[a-zA-Z_][a-zA-Z0-9_]*/, token: "variable"},
        {regex: /[\{\}\(\)\[\]]/, token: null},
        {regex: /==|!=|<=|>=|<|>|\+|\-|\*|\/|=/, token: "operator"},
      ],
      meta: {
        dontIndentStates: ["comment"],
        lineComment: "//"
      }
    });

    // Inicializa editor CodeMirror com modo customizado e tema personalizado
    const editor = CodeMirror.fromTextArea(document.getElementById('codigo'), {
      lineNumbers: true,
      mode: "alexMode",
      theme: "alex-theme",
      tabSize: 2,
      indentUnit: 2,
      autofocus: true,
    });

    const btn = document.getElementById('btnExecutar');
    const terminal = document.getElementById('terminal');
    const sessao_id = 'sessao_web';

    btn.addEventListener('click', async () => {
      const codigo = editor.getValue().trim();
      if (!codigo) {
        alert('Por favor, digite algum código.');
        return;
      }

      terminal.textContent = 'Executando...\n';

      try {
        const response = await fetch('/executar', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({ sessao_id, codigo })
        });

        const data = await response.json();
        terminal.textContent = data.saidas ? data.saidas.join('\n') : 'Nenhuma saída.';
      } catch (err) {
        terminal.textContent = 'Erro: ' + err.message;
      }
    });

// No seu JavaScript
fetch('/nova-sessao', { method: 'POST' })
  .then(response => response.json())
  .then(data => {
    const sessaoId = data.sessao_id;
    // Armazene o sessionId para usar nas requisições
  });