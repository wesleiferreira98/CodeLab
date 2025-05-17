import re

# Definindo os tipos permitidos
TIPOS = {
    'numero': int,
    'decimal': float,
    'letra': str,
    'palavra': str
}

# Tabela de variáveis
variaveis = {}
tipos_variaveis = {}
condicao_atendida_atual=False
condicao_atendida=False
# Verificando compatibilidade de tipos
def verificar_compatibilidade(tipo, valor):
    try:
        # Avaliando a expressão para verificar tipos
        resultado = eval(valor, {}, variaveis)
        if isinstance(resultado, TIPOS[tipo]):
            return resultado
        else:
            raise TypeError(f"Operação inválida entre tipos: {type(resultado).__name__}, {TIPOS[tipo].__name__}")
    except Exception as e:
        raise TypeError(f"Erro ao avaliar a expressão '{valor}': {e}")

# Função para interpretar declaração de variáveis
def interpretar_variavel(linha):
    match = re.match(r"(numero|decimal|letra|palavra)\s+(\w+)\s*=\s*(.+);", linha)
    if match:
        tipo, nome, valor = match.groups()
        if tipo in TIPOS:
            try:
                resultado = verificar_compatibilidade(tipo, valor)
                variaveis[nome] = resultado
                tipos_variaveis[nome] = tipo
                print(f"Variável '{nome}' definida como {variaveis[nome]} ({tipo})")
            except TypeError as e:
                print(f"Erro de tipo ao definir variável '{nome}': {e}")
            except Exception as e:
                print(f"Erro ao definir variável '{nome}': {e}")
        else:
            print(f"Tipo '{tipo}' não é suportado.")
    else:
        print(f"Erro de sintaxe na declaração: {linha}")

# Função para interpretar comandos de saída
def interpretar_escrever(linha):
    match = re.match(r"Escrever\((.+)\);", linha)
    if match:
        mensagem = match.group(1)
        try:
            print(eval(mensagem, {}, variaveis))
        except Exception as e:
            print(f"Erro ao processar comando Escrever: {e}")
    else:
        print(f"Erro de sintaxe no comando Escrever: {linha}")

# Função para interpretar comandos de entrada
def interpretar_ler(linha):
    match = re.match(r"Ler\((\w+)\);", linha)
    if match:
        nome_variavel = match.group(1)
        if nome_variavel in variaveis:
            novo_valor = input(f"Digite o valor para '{nome_variavel}': ")
            try:
                variaveis[nome_variavel] = type(variaveis[nome_variavel])(novo_valor)
            except ValueError:
                print(f"Valor inválido para a variável '{nome_variavel}'")
        else:
            print(f"Variável '{nome_variavel}' não foi definida.")
    else:
        print(f"Erro de sintaxe no comando Ler: {linha}")

# Função para interpretar estruturas de controle Se, Senao se, Senao
def interpretar_condicional(linhas, start_index):
    global condicao_atual
    global executar_bloco
    global bloco_atual
    global dentro_de_condicao
    global condicao_atendida
    global linha_atual_global  # Para rastrear a linha atual no loop principal

    condicao_atual = None
    executar_bloco = False
    bloco_atual = []
    dentro_de_condicao = False
    i = start_index

    while i < len(linhas):
        linha = linhas[i].strip()
        linha_atual_global = i  # Atualiza a linha atual globalmente

        print(f"\n[CONDICIONAL] Analisando linha {i+1}: '{linha}'")
        print(f"  condicao_atual: {condicao_atual}, executar_bloco: {executar_bloco}, dentro_de_condicao: {dentro_de_condicao}, condicao_atendida: {condicao_atendida}, variaveis: {variaveis}")

        if linha.startswith("Se("):
            if not condicao_atendida:
                match = re.match(r"Se\((.+?)\)\s*\{", linha)
                if match:
                    condicao = match.group(1).strip()
                    print(f"  [CONDICIONAL] Condição Se encontrada: '{condicao}'")
                    try:
                        resultado_condicao = eval(condicao, {}, variaveis)
                        if resultado_condicao:
                            executar_bloco = True
                            condicao_atual = 'Se'
                            bloco_atual = []
                            dentro_de_condicao = True
                            
                            print("  [CONDICIONAL] Condição Se avaliada como VERDADEIRA.")
                        else:
                            executar_bloco = False
                            dentro_de_condicao = True
                            
                            print("  [CONDICIONAL] Condição Se avaliada como FALSA.")
                    except Exception as e:
                        print(f"  [CONDICIONAL] Erro ao avaliar condição Se: {e}")
                else:
                    print(f"  [CONDICIONAL] Erro de sintaxe na condição Se: {linha}")
            else:
                print("  [CONDICIONAL] Bloco Se ignorado (condição anterior já atendida).")
                nivel = 1
                i += 1
                while i < len(linhas):
                    linha_interna = linhas[i].strip()
                    if linha_interna.endswith("{"):
                        nivel += 1
                    elif linha_interna == "}":
                        nivel -= 1
                        if nivel == 0:
                            break
                    i += 1
                condicao_atual = None
                continue

        elif linha.startswith("Senao se("):
            condicao_atual = 'Senao se'
            if not condicao_atendida:
                match = re.match(r"Senao se\((.+?)\)\s*\{", linha)
                if match:
                    condicao = match.group(1).strip()
                    print(f"  [CONDICIONAL] Condição Senao se encontrada: '{condicao}'")
                    try:
                        resultado_condicao = eval(condicao, {}, variaveis)
                        print("Resultado da condição ",resultado_condicao)
                        print("Resultado geral ", not executar_bloco and condicao_atual in ['Se', 'Senao se'] and resultado_condicao)
                        print("Resultado do executar bloco ", not executar_bloco)
                        if not executar_bloco and resultado_condicao:
                            executar_bloco = True
                            condicao_atual = 'Senao se'
                            bloco_atual = []
                            dentro_de_condicao = True
                            print("  [CONDICIONAL] Condição Senao se avaliada como VERDADEIRA.")
                        else:
                            executar_bloco = False
                            dentro_de_condicao = True
                            condicao_atual = None
                            print("  [CONDICIONAL] Condição Senao se avaliada como FALSA (ou bloco anterior já executado).")
                    except Exception as e:
                        print(f"  [CONDICIONAL] Erro ao avaliar condição Senao se: {e}")
                else:
                    print(f"  [CONDICIONAL] Erro de sintaxe na condição Senao se: {linha}")
            else:
                print("  [CONDICIONAL] Bloco Senao se ignorado (condição anterior já atendida).")
                nivel = 1
                i += 1
                while i < len(linhas):
                    linha_interna = linhas[i].strip()
                    if linha_interna.endswith("{"):
                        nivel += 1
                    elif linha_interna == "}":
                        nivel -= 1
                        if nivel == 0:
                            break
                    i += 1
                condicao_atual = None
                continue

        elif linha.startswith("Senao{"):
            print("Condição atendida ", condicao_atendida)
            condicao_atual='Senao'
            if not condicao_atendida and condicao_atual in ['Se', 'Senao se','Senao']:
                if not executar_bloco:
                    executar_bloco = True
                    condicao_atual = 'Senao'
                    bloco_atual = []
                    dentro_de_condicao = True
                    print("  [CONDICIONAL] Bloco Senao encontrado.")
                else:
                    dentro_de_condicao = True
                    print("  [CONDICIONAL] Bloco Senao ignorado (bloco anterior já executado ou condição não apropriada).")
            else:
                print("  [CONDICIONAL] Bloco Senao ignorado (condição anterior já atendida).")
                nivel = 1
                i += 1
                while i < len(linhas):
                    linha_interna = linhas[i].strip()
                    if linha_interna.endswith("{"):
                        nivel += 1
                    elif linha_interna == "}":
                        nivel -= 1
                        if nivel == 0:
                            break
                    i += 1
                condicao_atual = None
                continue

        elif linha == "}":
            print("  [CONDICIONAL] Fechamento de bloco encontrado.")
            if executar_bloco:
                print("  [CONDICIONAL] Executando bloco...")
                for comando in bloco_atual:
                    comando_limpo = comando.strip()
                    if comando_limpo:
                        condicao_atendida=True
                        print(f"    [CONDICIONAL] Executando comando: '{comando_limpo}'")
                        if comando_limpo.startswith("Escrever"):
                            interpretar_escrever(comando_limpo)
                        elif comando_limpo.startswith("Ler"):
                            interpretar_ler(comando_limpo)
                        elif re.match(r"(numero|decimal|letra|palavra)\s+\w+\s*=\s*.+;", comando_limpo):
                            interpretar_variavel(comando_limpo)
                condicao_atendida = True
                print("  [CONDICIONAL] Bloco executado.")
            condicao_atual = None
            executar_bloco = False
            bloco_atual = []
            dentro_de_condicao = False
            print("  [CONDICIONAL] Variáveis de controle resetadas.")
            return i + 1 # Retorna o índice da próxima linha após o bloco

        elif executar_bloco and dentro_de_condicao:
            print(f"  [CONDICIONAL] Adicionando ao bloco atual: '{linha}'")
            bloco_atual.append(linha)

        i += 1
    return i

# Variável global para rastrear a linha atual
linha_atual_global = 0
# Função para interpretar loops 'Enquanto'
def interpretar_enquanto(linhas, start_index):
    match = re.match(r"Enquanto\((.+)\)\s*{", linhas[start_index])
    if match:
        condicao = match.group(1)
        bloco = []
        i = start_index + 1
        while i < len(linhas) and not linhas[i].strip().startswith("}"):
            bloco.append(linhas[i])
            i += 1
        if i == len(linhas):
            print(f"Erro: bloco 'Enquanto' não fechado corretamente.")
            return i
        while eval(condicao, {}, variaveis):
            for comando in bloco:
                comando = comando.strip()
                if comando.startswith("Escrever"):
                    interpretar_escrever(comando)
                elif comando.startswith("Ler"):
                    interpretar_ler(comando)
                elif re.match(r"(numero|decimal|letra|palavra)\s+\w+\s*=\s*.+;", comando):
                    interpretar_variavel(comando)
                elif re.match(r"\w+\s*=\s*.+;", comando):
                    interpretar_variavel(f"{tipos_variaveis[comando.split('=')[0].strip()]} {comando}")
                elif comando.startswith("Se"):
                    interpretar_condicional([comando])
        return i + 1
    else:
        print(f"Erro de sintaxe no comando 'Enquanto': {linhas[start_index]}")
        return start_index + 1


# Função principal para interpretar o código
def interpretar(linhas):
    global linha_atual_global
    while linha_atual_global < len(linhas):
        linha = linhas[linha_atual_global].strip()
        print(f"\n[PRINCIPAL] Analisando linha {linha_atual_global + 1}: '{linha}'")
        if linha.startswith("numero") or linha.startswith("decimal") or linha.startswith("letra") or linha.startswith("palavra"):
            interpretar_variavel(linha)
            linha_atual_global += 1
        elif linha.startswith("Escrever"):
            interpretar_escrever(linha)
            linha_atual_global += 1
        elif linha.startswith("Ler"):
            interpretar_ler(linha)
            linha_atual_global += 1
        elif linha.startswith("Se(") or linha.startswith("Senao se(") or linha.startswith("Senao{"):
            linha_atual_global = interpretar_condicional(linhas, linha_atual_global)
        elif linha.startswith("Enquanto"):
            linha_atual_global = interpretar_enquanto(linhas, linha_atual_global)
        else:
            linha_atual_global += 1 # Ignora linhas não reconhecidas

# Testando o código
linhas_teste = [
    "numero idade = 15;",
    "palavra nome = 'Weslei';",
    "Escrever('O aluno se chama ' + nome + ' e tem ' + str(idade) + ' anos.');",
    "numero soma = idade + 5;",
    "Escrever(soma);",
    "palavra texto = nome + ' tem ' + str(idade) + ' anos';",
    "Escrever(texto);",
    "Enquanto(idade < 18){",
    "    idade = idade + 1;",
    "    Escrever('Idade atualizada para ' + str(idade));",
    "}",
    "Escrever('Loop terminado. Idade final: ' + str(idade));"
]


interpretar(linhas_teste)

print("\nEstado final das variáveis:", variaveis)