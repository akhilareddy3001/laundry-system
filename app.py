from flask import Flask, request, jsonify
import uuid
app = Flask(__name__)
orders = []
@app.route('/')
def home():
    return "Laundary API is running!"
@app.route('/create_order', methods=['POST'])
def create_order():
    data = request.json
    total = 0
    for item in data['items']:
        total += item['quantity'] * item['price']
    order = {
        'id': str(uuid.uuid4()),
        'name': data['name'],
        'phone': data['phone'],
        'items': data['items'],
        'total': total,
        'status': 'RECEIVED'
    }
    orders.append(order)
    return jsonify(order), 201
@app.route('/orders', methods=['GET'])
def get_orders():
    return jsonify(orders), 200
@app.route('/update_status/<order_id>', methods=['PUT'])
def update_status(order_id):    
    data = request.json
    for order in orders:
        if order['id'] == order_id:
            order['status'] = data['status']
            return jsonify(order), 200
    return jsonify({'error': 'Order not found'}), 404

@app.route('/dashboard', methods=['GET'])
def dashboard():
    total_orders = len(orders)
    revenue = sum(order['total'] for order in orders)
    status_counts = {}
    for order in orders:
        status = order['status']
        if status not in status_counts:
            status_counts[status] = 0
        status_counts[status] += 1
    return jsonify({
        'total_orders': total_orders,
        'revenue': revenue,
        'status_counts': status_counts
    }), 200
if __name__ == '__main__':
    app.run(debug=True)
