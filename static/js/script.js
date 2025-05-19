// Definir palavras reservadas para o pseudocódigo
    const palavrasReservadas = [
      "Escrever", "Ler", "numero", "decimal", "texto", "Se", "Senao", "Enquanto", "FimSe", "FimEnquanto", "Parar","palavra","letra"
    ];

    // Registrar o modo personalizado para o CodeMirror
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

    // Inicializa o editor CodeMirror
    const editor = CodeMirror.fromTextArea(document.getElementById('codigo'), {
      lineNumbers: true,
      mode: "alexMode",
      theme: "alex-theme",
      tabSize: 2,
      indentUnit: 2,
      autofocus: true,
    });

    let sessaoId = '';

    // Cria uma nova sessão ao carregar a página
    async function iniciarSessao() {
        try {
            const response = await fetch('/nova-sessao', { method: 'POST' });
            const data = await response.json();
            sessaoId = data.sessao_id;
            console.log('Sessão iniciada:', sessaoId);
        } catch (err) {
            console.error('Erro ao iniciar sessão:', err);
            alert('Erro ao iniciar sessão. Tente novamente.');
        }
    }

    // Chama a função para iniciar a sessão
    iniciarSessao();

    // Executa o código quando o botão é clicado
    const btn = document.getElementById('btnExecutar');
    const terminal = document.getElementById('terminal');

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
                body: JSON.stringify({ sessao_id: sessaoId, codigo })
            });

            const data = await response.json();
            terminal.textContent = data.saidas ? data.saidas.join('\n') : 'Nenhuma saída.';
        } catch (err) {
            terminal.textContent = 'Erro: ' + err.message;
        }
    });