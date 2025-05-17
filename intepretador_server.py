import re
from flask import jsonify
import io
from contextlib import redirect_stdout
class SessaoInterpretador:
    TIPOS = {
        'numero': int,
        'decimal': float,
        'letra': str,
        'palavra': str
    }

    def __init__(self, sessao_id):
        self.sessao_id = sessao_id
        self.variaveis = {}
        self.tipos_variaveis = {}
        self.saidas = []
        self.erros = []
        self.pendente_ler = None

    def reiniciar(self):
        self.__init__(self.sessao_id)

    def processar_codigo(self, codigo):
        self.reiniciar()
        try:
            codigo_python_str =  self._converter_para_python(codigo)
            print(f"[DEBUG] Código Python gerado:\n{codigo_python_str}")

            # Captura a saída do código Python gerado
            f = io.StringIO()
            with redirect_stdout(f):
                exec(codigo_python_str, self.variaveis)
            saidas = f.getvalue().strip().split('\n') if f.getvalue() else []

            self.saidas = saidas

            return self._responder_sucesso()

        except Exception as e:
            self.erros.append(f"Erro fatal: {str(e)}")
            return self._responder_erro()


    def _converter_para_python1(self, codigo):
        linhas = [linha.strip() for linha in codigo.split('\n') if linha.strip()]
        codigo_python = []
        indent_level = 0
        indent_str = '    '  # 4 espaços

        for linha in linhas:
            # Detecta fechamento de bloco (}) e reduz indentação
            if linha == '}':
                indent_level = max(indent_level - 1, 0)
                continue

            # Detecta abertura de bloco ({ no final da linha)
            if linha.endswith('{'):
                linha_sem_chave = linha[:-1].strip()
                linha_convertida = self._converter_linha(linha_sem_chave)
                codigo_python.append(indent_str * indent_level + linha_convertida)
                indent_level += 1
                continue

            # Linha normal, converte e adiciona com indentação atual
            linha_convertida = self._converter_linha(linha)
            codigo_python.append(indent_str * indent_level + linha_convertida)

        return "\n".join(codigo_python)
    def _converter_para_python(self, codigo):
        linhas = [linha.strip() for linha in codigo.split('\n') if linha.strip()]
        codigo_python = []
        indent_level = 0
        indent_str = '    '

        for linha in linhas:
            # Contar quantos fechamentos de bloco existem na linha
            close_braces = linha.count('}')
            if close_braces > 0:
                indent_level = max(indent_level - close_braces, 0)
                linha = linha.replace('}', '')  # Remove os fechamentos

            # Converter a linha
            if linha.endswith('{'):
                linha_sem_chave = linha[:-1].strip()
                converted = self._converter_linha(linha_sem_chave)
                codigo_python.append(indent_str * indent_level + converted)
                indent_level += 1
            else:
                converted = self._converter_linha(linha)
                codigo_python.append(indent_str * indent_level + converted)

        return "\n".join(codigo_python)

    def _converter_linha(self, linha):
        # Trata declarações de variáveis com tipo (numero, decimal, letra, palavra)
        if linha.startswith(("numero", "decimal", "letra", "palavra")):
            return self._converter_variavel(linha)
        
        # Trata comando Escrever()
        elif linha.startswith("Escrever("):
            return self._converter_escrever(linha)
        
        # Trata comando Ler()
        elif linha.startswith("Ler("):
            return self._converter_ler(linha)
        
        # Trata comandos condicionais (Se, Senao se, Senao)
        elif linha.startswith("Se(") or linha.startswith("Senao se(") or linha.startswith("Senao"):
            return self._converter_condicional(linha)
        
        # Trata comandos de loop (Enquanto)
        elif linha.startswith("Enquanto("):
            return self._converter_enquanto(linha)

        elif linha.strip() == "Parar;":
            return "break"
        
        # Trata atribuições simples (ex: x = x + 1;)
        elif re.match(r"^\w+\s*=\s*.+;$", linha):
            # Remove o ponto e vírgula e retorna a linha convertida
            return linha[:-1].strip()
        
        # Comando não reconhecido
        else:
            self.erros.append(f"Comando não reconhecido: {linha}")
            return ""


    def _converter_variavel(self, linha):
        # Declaração de variáveis (com tipo)
        match = re.match(r"(numero|decimal|letra|palavra)\s+(\w+)\s*=\s*(.+);", linha)
        if match:
            tipo, nome, valor = match.groups()
            self.tipos_variaveis[nome] = tipo
            return f"{nome} = {valor}"

        # Atribuição simples (variável já declarada)
        match = re.match(r"(\w+)\s*=\s*(.+);", linha)
        if match:
            nome, valor = match.groups()
            # Se variável não declarada, dá warning, mas gera código mesmo assim
            if nome not in self.tipos_variaveis:
                self.erros.append(f"Variável não declarada: {nome}")
            return f"{nome} = {valor}"

        self.erros.append(f"Erro de sintaxe na declaração de variável: {linha}")
        return ""


    def _converter_escrever(self, linha):
        match = re.match(r"Escrever\((.+)\);", linha)
        if match:
            return f"print({match.group(1)})"
        self.erros.append(f"Erro de sintaxe em Escrever(): {linha}")
        return ""

    def _converter_ler(self, linha):
        match = re.match(r"Ler\((\w+)\);", linha)
        if match:
            nome = match.group(1)
            
            # Verifica se a variável foi declarada antes de tentar ler
            if nome not in self.tipos_variaveis:
                self.erros.append(f"Variável não declarada: {nome}")
                return ""
            
            # Marca a variável como pendente para leitura
            self.pendente_ler = nome
            
            # Cria uma entrada para a variável no estado
            if nome not in self.variaveis:
                tipo = self.TIPOS[self.tipos_variaveis[nome]]
                self.variaveis[nome] = tipo()
            
            # Não gera código Python, apenas retorna o placeholder para evitar erro de execução
            return f"# Ler({nome}) - aguardando entrada do usuário"
        
        self.erros.append(f"Erro de sintaxe em Ler(): {linha}")
        return ""



    def _converter_condicional(self, linha):
        linha = linha.strip()
        # Verifica Senão com acento
        if linha.startswith("Se("):
            condicao = re.search(r"Se\((.*?)\)", linha).group(1)
            return f"if {condicao}:"
        elif linha.startswith("Senao Se("):  # Com acento
            condicao = re.search(r"Senao Se\((.*?)\)", linha).group(1)
            return f"elif {condicao}:"
        elif linha == "Senao":  # Com acento e sem condição
            return "else:"
        else:
            self.erros.append(f"Erro de sintaxe em condicional: {linha}")
            return ""

    def _converter_enquanto(self, linha):
        condicao = re.search(r"Enquanto\((.*?)\)", linha)
        if condicao:
            return f"while {condicao.group(1)}:"
        self.erros.append(f"Erro de sintaxe em Enquanto(): {linha}")
        return ""

    def _responder_sucesso(self):
        return jsonify({
            'sessao_id': self.sessao_id,
            'saidas': self.saidas,
            'erros': self.erros,
            'pendente_input': self.pendente_ler if self.pendente_ler else None,
            'finalizado': not self.pendente_ler
        })


    def _responder_erro(self):
        return jsonify({
            'sessao_id': self.sessao_id,
            'saidas': self.saidas,
            'erros': self.erros,
            'pendente_input': self.pendente_ler if self.pendente_ler else None,
            'finalizado': not self.pendente_ler
        }), 400

