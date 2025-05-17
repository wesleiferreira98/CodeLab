
## **CodeLab - Ambiente de Pseudocódigo Educacional**

O **CodeLab** é uma plataforma online para ensinar e praticar pseudocódigo de forma interativa, desenvolvida para facilitar o aprendizado de lógica de programação. Inspirada em ferramentas como Replit e ambientes de codificação online, o **CodeLab** oferece um editor de código, terminal de saída e uma interface intuitiva para iniciantes em programação.

###  **Funcionalidades Principais**

* **Editor de Código:** Área dedicada para escrever pseudocódigo, com destaque de sintaxe.
* **Terminal de Saída:** Exibe os resultados do código executado em tempo real.
* **Suporte a Pseudocódigo Alex:** Interpreta uma linguagem de pseudocódigo desenvolvida especificamente para facilitar a transição para linguagens como C++ e Python.
* **Design Responsivo:** Interface adaptada para diferentes tamanhos de tela.
* **Botão de Execução Rápida:** Permite testar o código imediatamente.

---

###  **Estrutura do Projeto**

```
CodeLab/
├── app.py                       # Arquivo principal do Flask
├── intepretador.py              # Lógica do interpretador de pseudocódigo
├── intepretador_server.py       # Lógica do servidor Flask
├── main.py                      # Ponto de entrada do servidor (opcional)
├── __pycache__/                 # Cache do Python (ignorar no git)
├── static/
│   ├── css/
│   │   ├── bootstrap.min.css
│   │   ├── codemirror.min.css
│   │   └── styles.css          # Estilos personalizados
│   ├── img/                    # Imagens do projeto
│   └── js/
│       ├── bootstrap.bundle.min.js
│       ├── codemirror.min.js
│       ├── javascript.min.js
│       ├── simple.min.js
│       └── script.js           # Script principal do CodeLab
├── templates/
│   ├── index.html              # Página inicial do ambiente
│   ├── desafios.html           # Página de desafios (opcional)
│   └── sobre.html              # Página sobre (opcional)
├── tests/
│   ├── test_interpretador.py   # Testes do interpretador
│   └── test_server.py          # Testes do servidor
├── requirements.txt            # Dependências do projeto (Flask, etc)
└── README.md                   # Documentação do projeto
```

---

###  **Dependências**

Para rodar o projeto, você precisará das seguintes bibliotecas Python:

* **Flask** (Servidor web)
* **CodeMirror** (Editor de código)
* **Bootstrap** (Estilos)

Instale todas as dependências com:

```bash
pip install -r requirements.txt
```

---

###  **Como Executar o Projeto**

1. **Clone o repositório:**

```bash
git clone https://github.com/seu-usuario/CodeLab.git
cd CodeLab
```

2. **Instale as dependências:**

```bash
pip install -r requirements.txt
```

3. **Execute o servidor:**

```bash
python app.py
```

4. **Acesse a aplicação:**

Abra o navegador e acesse  **[http://localhost:5000](http://localhost:5000/)** .

---

###  **Estrutura dos Arquivos**

* **app.py:** Configura o servidor Flask e define as rotas.
* **intepretador.py:** Implementa a lógica para interpretação do pseudocódigo.
* **intepretador_server.py:** Configura a API para interação com o interpretador.
* **static/css:** Arquivos de estilo.
* **static/js:** Scripts para interação do editor.
* **templates:** Páginas HTML que compõem a interface do CodeLab.

###  **Testes**

Para executar os testes, use:

```bash
python -m unittest discover tests/
```

---

###  **Futuras Implementações**

* Integração com uma API para salvar o progresso dos alunos.
* Módulo de desafios com pontuação automática.
* Feedback em tempo real para sugestões de melhoria no código.

---

###  **Contribuições**

Contribuições são bem-vindas! Sinta-se à vontade para abrir uma *Issue* ou enviar um *Pull Request* com melhorias ou correções.

---

###  **Licença**

Este projeto é distribuído sob a licença MIT. Veja o arquivo [LICENSE](https://chatgpt.com/c/LICENSE) para mais detalhes.

---

Quer que eu também prepare um exemplo de `requirements.txt` para você?
