import requests
import json

# Configurações
BASE_URL = 'http://localhost:5000'
HEADERS = {'Content-Type': 'application/json'}

def testar_interpretador():
    # Helper function para executar código
    def executar_codigo(sessao_id, codigo):
        url = f'{BASE_URL}/executar'
        payload = {
            'sessao_id': sessao_id,
            'codigo': codigo
        }
        return requests.post(url, data=json.dumps(payload), headers=HEADERS)

    # Helper function para enviar input
    def enviar_input(sessao_id, valor):
        url = f'{BASE_URL}/input'
        payload = {
            'sessao_id': sessao_id,
            'valor': valor
        }
        return requests.post(url, data=json.dumps(payload), headers=HEADERS)

    # Teste 1: Criação de sessão e código básico
    print("\n=== Teste 1: Declaração de variáveis e output ===")
    sessao_id = 'teste1'
    codigo = '''
    numero idade = 25;
    palavra nome = "Ana";
    Escrever(nome + " tem " + str(idade) + " anos");
    '''
    response = executar_codigo(sessao_id, codigo).json()
    print("Saídas recebidas:", response['saidas'])
    assert 'Ana tem 25 anos' in response['saidas'], "Teste 1 falhou!"
    print("✓ Teste 1 passou")

    # Teste 2: Condicionais e loops
    sessao_id = 'teste2'
    codigo = '''
    numero x = 1;
    Enquanto(x < 3){
        Escrever("Valor atual: " + str(x));
        x = x + 1;
    }
    Se(x == 3){
        Escrever("Loop completo!");
    }
    '''
    response = executar_codigo(sessao_id, codigo).json()
    assert response['saidas'] == ['Valor atual: 1', 'Valor atual: 2', 'Loop completo!'], print("Teste 2 falhou!", response['saidas'])
    print("✓ Teste 2 passou")

    # Teste 3: Input e tratamento de erros
    print("\n=== Teste 3: Input e erros ===")
    sessao_id = 'teste3'
    codigo = '''
    numero valor;
    Ler(valor);
    Escrever("Dobro: " + str(valor * 2));
    '''
    # Teste 4: Erros de sintaxe
    print("\n=== Teste 4: Erros de sintaxe ===")
    sessao_id = 'teste4'
    codigo = 'Escrever("Oi"'

    response = executar_codigo(sessao_id, codigo).json()
    print("Saídas recebidas:", response['erros'])
    assert 'Erro de sintaxe' in response['erros'][0]


    print("✓ Teste 4 passou")

if __name__ == '__main__':
    testar_interpretador()
    print("\nTodos os testes passaram com sucesso!")