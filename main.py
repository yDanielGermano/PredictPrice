import requests

IOF = 1.035

IMPOSTOS_ESTADOS = {
    "SP": 1.18,
    "MG": 1.17,
    "RJ": 1.22,
    "SC": 1.17,
    "PR": 1.17,
    "AC": 1.20,
    "AL": 1.20,
    "AM": 1.17,
    "AP": 1.18,
    "BA": 1.20,
    "CE": 1.20,
    "DF": 1.17,
    "ES": 1.17,
    "GO": 1.17,
    "MA": 1.17,
    "MT": 1.17,
    "MS": 1.17,
    "PA": 1.19,
    "PB": 1.20,
    "PE": 1.17,
    "PI": 1.20,
    "RN": 1.20,
    "RO": 1.17,
    "RR": 1.20,
    "RS": 1.17,
    "SE": 1.20,
    "TO": 1.17
}

IMPOSTOS_CATEGORIA = {
    "hardware": 1.60,
    "games": 1.15,
    "roupas": 1.25,
    "alimentos": 1.10,
    "livros": 1.00
}


def precificador_pro():
    print("\n--- Precificador Pro --- ")
    try:
    # 1. Converte para Real
        multiplicador_categoria = input("\nDigite a categoria do produto (hardware, games, roupas, alimentos, livros): ").lower()
    except ValueError:
        print("Entrada inválida. Por favor, tente novamente.")
        return
    if multiplicador_categoria in IMPOSTOS_CATEGORIA:
        taxa_categoria = IMPOSTOS_CATEGORIA[multiplicador_categoria]
    else:
        print("Categoria não encontrada. Digite uma categoria válida.")
        return
    try:
        preco_base_usd = float(input("Digite o preço base do produto em USD: "))
    except ValueError:
        print("Entrada inválida. Por favor, tente novamente.")
        return
    try:
        estado = input("Digite o estado de destino do produto (sigla): ").upper()
    except ValueError:
        print("Entrada inválida. Por favor, tente novamente.")
        return
    if estado in IMPOSTOS_ESTADOS:
        taxa_icms = IMPOSTOS_ESTADOS[estado]
    else:
        print("Estado não encontrado. Digite uma sigla de estado válida.")
        return
    cotacao = pegar_dolar()
    valor_real = preco_base_usd * cotacao
    
    # 2. Aplica o IOF do cartão (3.5%)
    valor_com_iof = valor_real * IOF
    
    # 3. Aplica a Categoria (II simplificado)
    
    valor_com_categoria_e_iof = valor_com_iof * taxa_categoria
    
    # 4. Aplica o ICMS do Estado que você pegou do GOV
    # (O ICMS no Brasil é calculado 'por dentro', mas para o seu app, 
    # use a soma simples para não bugar a cabeça agora)
    valor_final = valor_com_categoria_e_iof * taxa_icms
    return print(f"O valor do produto em {estado} é: R$ {valor_final:.2f}")

def pegar_dolar():
    try:
        url = "https://economia.awesomeapi.com.br/last/USD-BRL"
        res = requests.get(url, timeout=5)
        print(f"Conexão OK! O dólar agora está: R$ {res.json()['USDBRL']['bid']}")
        return float(res.json()['USDBRL']['bid'])
    except:
        return 5.25 # Valor de segurança
    
def exercicio_alan():
    print("\n--- Calculadora básica de preço final do consumidor--- ")
    try:
        preco_base = input("\nDigite o preço base do produto: ")
        preco_base_conv = float(preco_base)
        imposto_fixo = 0.35 * preco_base_conv
        margem_lucro = 0.10 * (preco_base_conv + imposto_fixo)
        valor_final = preco_base_conv + imposto_fixo + margem_lucro
        print(f"\nPreço de venda final do produto: {valor_final:.2f}")
    except ValueError:
        print("Entrada inválida. Por favor, tente novamente.")

def main():
    # Esta é a sua função "maestra". Ela controla o fluxo.
    while True:
        print("SISTEMAS DE CALCULO PARA PRODUTOS FINAL - DANIEL G.")
        print("\n" + "=" * 30)
        print("\n1 - Tarefa Fatec  \n2 - Precificador Pro  \n0 - Sair")
        try:
            opcao = input("Escolha: ")
            
            if opcao == "1":
                exercicio_alan()
            elif opcao == "2":
                precificador_pro()
            elif opcao == "0":
                break
        except ValueError:
            print("Entrada inválida. Por favor, tente novamente.")

if __name__ == "__main__":
    main()