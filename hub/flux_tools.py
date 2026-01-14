import requests

def discovery_ucp(url: str):
    url = url.replace("localhost", "127.0.0.1")
    base_url = url.split('/api/v1')[0].rstrip('/')
    target_url = f"{base_url}/.well-known/ucp"
    try:
        response = requests.get(target_url, timeout=5)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def create_checkout(url: str, items: list[str]):
    url = url.replace("localhost", "127.0.0.1")
    base_url = url.split('/api/v1')[0].rstrip('/')
    target_url = f"{base_url}/api/v1/checkout"
    try:
        response = requests.post(target_url, json={"items": items}, timeout=5)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def authorize_payment(url: str, checkout_id: str, amount: float):
    """
    Usa o mandato do usuário para autorizar e realizar o pagamento.
    """
    url = url.replace("localhost", "127.0.0.1")
    base_url = url.split('/api/v1')[0].rstrip('/')
    target_url = f"{base_url}/api/v1/pay"
    
    print(f"💳 [FLUX_TOOLS] Autorizando R$ {amount} para o pedido {checkout_id}...")
    try:
        # Simulamos o envio do token de mandato do usuário
        payload = {"checkout_id": checkout_id, "amount": amount, "token": "MANDATO-MARIO-123"}
        response = requests.post(target_url, json=payload, timeout=5)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def check_payment_status(url: str, checkout_id: str):
    url = url.replace("localhost", "127.0.0.1")
    base_url = url.split('/api/v1')[0].rstrip('/')
    target_url = f"{base_url}/api/v1/status/{checkout_id}"
    try:
        response = requests.get(target_url, timeout=5)
        return response.json()
    except Exception as e:
        return {"error": str(e)}