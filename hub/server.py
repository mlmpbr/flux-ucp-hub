import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Importamos nosso conjunto de ferramentas UCP
from flux_tools import discovery_ucp, create_checkout, authorize_payment, check_payment_status

# 1. Configuração de Ambiente
load_dotenv(dotenv_path=Path(__file__).parent.parent / '.env')

API_KEY = os.getenv("GEMINI_API_KEY")

def start_flux():
    if not API_KEY:
        print("❌ ERRO: Chave GEMINI_API_KEY não encontrada no arquivo .env")
        return

    client = genai.Client(api_key=API_KEY)
    
    # 2. Registro das Ferramentas
    tools = [discovery_ucp, create_checkout, authorize_payment, check_payment_status]
    
    # Mapeamento para execução dinâmica
    funcs = {
        "discovery_ucp": discovery_ucp,
        "create_checkout": create_checkout,
        "authorize_payment": authorize_payment,
        "check_payment_status": check_payment_status
    }

    # 3. Inteligência de Agregação (System Instruction)
    # Aqui definimos o comportamento de "Varrer a Web" e "Comparar Preços"
    system_instruction = """
    Você é o AGENTE AGREGADOR FLUX. Sua missão é economizar o dinheiro do usuário.
    
    REGRAS DE OPERAÇÃO:
    1. ESCANEAMENTO: Você deve verificar as três lojas disponíveis nas URLs:
       - http://127.0.0.1:8182
       - http://127.0.0.1:8183
       - http://127.0.0.1:8184
    
    2. COMPARAÇÃO: Use 'discovery_ucp' em cada uma delas para ler os preços da 'Camiseta Navega'.
    
    3. DECISÃO: Escolha a loja que oferece o MENOR PREÇO.
    
    4. EXECUÇÃO (MANDATO): Você tem um mandato de R$ 200,00. 
       - Se o menor preço for inferior a R$ 200,00, siga para o checkout (create_checkout).
       - Após o checkout, use 'authorize_payment' para liquidar a fatura automaticamente.
       - Finalize usando 'check_payment_status' para garantir que o status é PAID.
    
    5. RELATÓRIO: Ao final, diga ao Mario em qual loja você comprou, o preço pago e o ID do pedido.
    """

    print("🚀 [FLUX HUB] Iniciando Agente Agregador...")
    print("📡 Escaneando ecossistema de mercantes (Portas 8182, 8183, 8184)...")
    print("-" * 60)

    # Criando o chat com a instrução de agregador
    chat = client.chats.create(
        model="gemini-2.5-flash", 
        config=types.GenerateContentConfig(
            tools=tools,
            system_instruction=system_instruction
        )
    )
    
    # Comando inicial do usuário
    prompt = "Encontre a melhor oferta para 'Camiseta Navega' e realize a compra completa usando meu mandato."
    
    response = chat.send_message(prompt)

    # 4. Loop de Execução de Agente (Pode disparar várias ferramentas por rodada)
    while any(part.function_call for part in response.candidates[0].content.parts):
        # O Gemini pode decidir chamar as 3 descobertas de uma vez só!
        for part in response.candidates[0].content.parts:
            if part.function_call:
                fn_name = part.function_call.name
                fn_args = part.function_call.args
                
                print(f"⚙️  [AGENTE] Executando: {fn_name} | Argumentos: {fn_args}")
                
                # Execução da ferramenta
                resultado = funcs[fn_name](**fn_args)
                
                # Devolve o resultado para o Gemini
                response = chat.send_message(
                    types.Part.from_function_response(name=fn_name, response=resultado)
                )

    # Resumo final da transação
    print("\n" + "═"*60)
    print(f"🤖 RELATÓRIO FLUX:\n{response.text}")
    print("═"*60 + "\n")

if __name__ == "__main__":
    try:
        start_flux()
    except Exception as e:
        print(f"❌ Erro crítico no Hub: {e}")