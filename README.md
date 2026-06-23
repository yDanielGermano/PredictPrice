# 🪙 TaxCalc Pro | D-Oryzon
> **Automatizador de Impostos & Conversão Cambial Inteligente**

Uma solução robusta de linha de comando (CLI) desenvolvida em **Python** para simplificar o complexo fluxo de tributação de produtos importados e estaduais no Brasil. O sistema realiza a integração em tempo real com APIs financeiras de cotação cambial e aplica uma matriz tributária dinâmica de acordo com a localização do destinatário e a categoria do item.

---

## 💼 O Problema de Negócio

Microempreendedores, importadores e empresas de comércio eletrônico enfrentam desafios diários ao tentar precificar mercadorias com precisão. As principais dores do mercado incluem:
* **Oscilação Cambial Contínua:** A variação do dólar comercial (USD) afeta diretamente o custo base.
* **Complexidade Tributária Multiestadual:** A variação de alíquotas de ICMS em cada um dos 26 estados brasileiros e Distrito Federal.
* **Tributação por Categoria de Produto:** A diferenciação de alíquotas e benefícios fiscais aplicados a diferentes tipos de mercadorias (ex: hardware vs. livros).

O cálculo manual consome tempo operacional precioso e é altamente suscetível a erros que geram prejuízos ou problemas com a conformidade fiscal.

---

## 🚀 A Solução (D-Oryzon)

O **TaxCalc Pro** centraliza e automatiza essa inteligência de cálculo em segundos por meio de uma interface interativa de terminal.

```
       [ Usuário insere Preço, Categoria e UF ]
                         │
                         ▼
        [ API de Cotação (AwesomeAPI) ] ──(Falha)──► [ Cotação de Segurança (R$ 5.25) ]
                         │
                      (Sucesso)
                         │
                         ▼
       [ Aplicação do IOF de Cartão (3.5%) ]
                         │
                         ▼
       [ Aplicação da Alíquota de Categoria ]
                         │
                         ▼
       [ Aplicação do ICMS Estadual de Destino ]
                         │
                         ▼
       [ Exibição do Preço Final Sugerido em R$ ]
```

---

## 🛠️ Lógica de Cálculo e Fluxo Tributário

O motor de cálculo do **TaxCalc Pro** segue uma estrutura cumulativa descrita pelas fórmulas matemáticas abaixo:

1. **Conversão Cambial (Base):**
   Converte o preço base em dólar americano para real utilizando a cotação em tempo real.
   \[
   \text{Valor Real} = \text{Preço Base (USD)} \times \text{Cotação USD-BRL}
   \]

2. **Incidência do IOF (Imposto sobre Operações Financeiras):**
   Aplica a taxa padrão para transações internacionais em cartão de crédito (definida no código como 3.5%).
   \[
   \text{Valor com IOF} = \text{Valor Real} \times 1.035
   \]

3. **Tributação da Categoria (II Simplificado):**
   Aplica um multiplicador com base no grupo tributário do produto:
   \[
   \text{Valor Tributado} = \text{Valor com IOF} \times \text{Multiplicador Categoria}
   \]

4. **Tributação Estadual (ICMS):**
   Aplica a alíquota final do ICMS do estado de destino sobre o valor cumulativo obtido anteriormente:
   \[
   \text{Preço Final} = \text{Valor Tributado} \times \text{Alíquota ICMS}
   \]

---

## 📦 Matriz Tributária Dinâmica

O sistema mapeia de forma estruturada as regras estaduais e setoriais através de dicionários estáticos integrados, permitindo fácil expansão:

### 1. Alíquotas de ICMS por Estado (Exemplos)
| Estado (UF) | Alíquota Aplicada | Estado (UF) | Alíquota Aplicada |
| :---: | :---: | :---: | :---: |
| **RJ** (Rio de Janeiro) | 22% (1.22) | **SP** (São Paulo) | 18% (1.18) |
| **MG** (Minas Gerais) | 17% (1.17) | **BA** (Bahia) | 20% (1.20) |
| **PA** (Pará) | 19% (1.19) | **DF** (Distrito Federal) | 17% (1.17) |

### 2. Multiplicadores por Categoria de Produto
| Categoria | Alíquota (II) | Multiplicador |
| :--- | :---: | :---: |
| **Hardware** | 60% | `1.60` |
| **Roupas** | 25% | `1.25` |
| **Games** | 15% | `1.15` |
| **Alimentos** | 10% | `1.10` |
| **Livros** (Imunidade constitucional) | 0% | `1.00` |

---

## 🔌 Integração e Consumo da API de Cotação

O sistema consome a **AwesomeAPI** (especificamente o endpoint `/last/USD-BRL`) de forma dinâmica.

* **Endpoint Utilizado:** `https://economia.awesomeapi.com.br/last/USD-BRL`
* **Campos de Retorno:** Captura o valor de compra (`bid`) em tempo real.
* **Resiliência e Fallback:** Se houver falha de conexão ou timeout na requisição à API, o sistema captura a exceção através de um bloco `try/except` e adota um **valor de segurança de R$ 5,25** para evitar interrupções no fluxo do usuário.

---

## ✨ Diferenciais Técnicos em Python

1. **Clean Code & SRP:**
   Funções com responsabilidade única facilitam a depuração e modularização. O código é segmentado em `pegar_dolar()`, `precificador_pro()`, e a execução da CLI é gerida pela função `main()`.
2. **Robustez no Tratamento de Erros:**
   * Utilização de blocos `try/except` com `ValueError` para entradas incorretas de tipos numéricos (ex: letras inseridas onde se esperavam floats).
   * Verificação de chaves (`in IMPOSTOS_ESTADOS` / `in IMPOSTOS_CATEGORIA`) para garantir que dados incorretos ou inexistentes não quebrem o fluxo, fornecendo feedback amigável ao usuário.
3. **Pronto para Escalabilidade:**
   A lógica de negócios e as tabelas de tributação estão completamente separadas da interface de entrada e saída. Isso viabiliza a migração futura do motor de cálculo para uma interface gráfica (Web, Mobile ou Desktop) ou backend de API (FastAPI/Flask) sem a necessidade de reescrever a lógica fiscal.

---

## 🚀 Como Executar o Projeto

Certifique-se de ter o Python 3.x e o gerenciador de pacotes `pip` instalados em sua máquina.

1. **Clonar o repositório:**
   ```bash
   git clone https://github.com/yDanielGermano/PredictPrice
   cd PredictPrice
   ```

2. **Instalar as dependências necessárias:**
   ```bash
   pip install requests
   ```

3. **Executar a aplicação:**
   ```bash
   python main.py
   ```

---

*Desenvolvido por **D-Oryzon** — Soluções Tecnológicas Automatizadas.*
