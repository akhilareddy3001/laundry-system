from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify
import uuid
app = Flask(__name__)
CORS(app,resources={r"/*": {"origins": "*"}})
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    items = db.Column(db.JSON, nullable=False)
    total = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='RECEIVED')
with app.app_context():
    db.create_all()


PRICE_LIST = {
    "shirt": 10,
    "pants": 15,
    "saree": 20,
    "tshirt": 8,
    "jeans": 18,
    "jacket": 25
}

@app.route('/')
def home():
    return "Laundary API is running!"
@app.route('/create_order', methods=['POST'])
def create_order():
    data = request.json
    items_with_price =[]
    total = 0
    for item in data['items']:
        cloth = item['type'].lower()
        price = PRICE_LIST.get(cloth, 10) 
        items_with_price.append({
            "type": cloth,
            "quantity": item['quantity'],
            "price": price
        })
        total += item['quantity'] * price
    order = Order(
        id=str(uuid.uuid4()),
        name=data['name'],
        phone=data['phone'],
        items=items_with_price,
        total=total,
        status='RECEIVED'
    )
    db.session.add(order)
    db.session.commit()
    print("SAVED TO DB")
    return jsonify({
        "message": "Order created successfully"
    })
    
@app.route('/orders', methods=['GET'])
def get_orders():
    orders = Order.query.all()
    result = []
    for o in orders:
        result.append({

            'id':o.id,
            'name':o.name,
            'phone':o.phone,
            'items':o.items,
            'total':o.total,
            'status':o.status
        })
    return jsonify(result)
@app.route('/update_status/<order_id>', methods=['PUT'])
def update_status(order_id):
    data = request.json

    order = Order.query.get(order_id)

    if not order:
        return jsonify({'error': 'Order not found'}), 404

    order.status = data['status']
    db.session.commit()

    return jsonify({
        "message": "Status updated"
    }), 200

@app.route('/dashboard', methods=['GET'])
def dashboard():
    orders = Order.query.all()

    total_orders = len(orders)
    revenue = sum(o.total for o in orders)

    status_counts = {}
    for o in orders:
        if o.status not in status_counts:
            status_counts[o.status] = 0
        status_counts[o.status] += 1

    return jsonify({
        'total_orders': total_orders,
        'revenue': revenue,
        'status_counts': status_counts
    }), 200
if __name__ == '__main__':
    app.run(debug=True)

       
