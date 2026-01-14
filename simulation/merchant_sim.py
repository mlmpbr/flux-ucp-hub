from flask import Flask, jsonify, request
import threading

def create_app(name, price, port):
    app = Flask(name)
    db = {}

    @app.route('/.well-known/ucp', methods=['GET'])
    def discovery():
        return jsonify({
            "merchant_name": name,
            "capabilities": {"checkout": "/api/v1/checkout", "payment": "/api/v1/pay", "status": "/api/v1/status"},
            "offers": [{"item": "Camiseta Navega", "price": price}] # Oferta explícita no Discovery
        })

    @app.route('/api/v1/checkout', methods=['POST'])
    def checkout():
        order_id = f"ORDER-{port}-XYZ"
        db[order_id] = {"status": "PENDING", "price": price}
        return jsonify({"checkout_id": order_id, "amount": price})

    @app.route('/api/v1/pay', methods=['POST'])
    def pay():
        data = request.json
        oid = data.get("checkout_id")
        if oid in db:
            db[oid]["status"] = "PAID"
            return jsonify({"status": "SUCCESS"})
        return jsonify({"status": "ERROR"}), 404

    @app.route('/api/v1/status/<oid>', methods=['GET'])
    def status(oid):
        return jsonify({"order_id": oid, "status": db.get(oid, {}).get("status", "NOT_FOUND")})

    def run():
        app.run(host='127.0.0.1', port=port, debug=False, use_reloader=False)
    
    return run

if __name__ == '__main__':
    # Iniciando as 3 lojas em threads separadas
    t1 = threading.Thread(target=create_app("Navega-Shop A", 150.0, 8182))
    t2 = threading.Thread(target=create_app("Navega-Shop B", 130.0, 8183))
    t3 = threading.Thread(target=create_app("Navega-Shop C", 170.0, 8184))
    
    t1.start(); t2.start(); t3.start()
    print("🚀 3 Lojas simuladas rodando nas portas 8182, 8183 e 8184!")