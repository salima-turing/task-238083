### Step 1: Import required modules
import mongokit
import pymongo
from datetime import datetime

from symengine import unicode

### Step 2: Initialize the MongoDB client

client = pymongo.MongoClient('mongodb+srv://salimao:nwaJx9prHGPzS4dM@turing.h9o7m.mongodb.net/?retryWrites=true&w=majority&appName=turing')

### Step 3: Create a MongoDB database and collection using 'mongokit'

db = client['logistics_db']
orders_collection = db.orders


### Step 4: Define a MongoKit model class for 'Order' data

class Order(mongokit.Document):
    use_dot_notation = True
    structure = {
        'order_id': unicode,
        'customer_name': unicode,
        'status': unicode,  # e.g., 'Pending', 'Shipped', 'Delivered'
        'location': {
            'city': unicode,
            'state': unicode,
            'country': unicode,
        },
        'tracking_number': unicode,
        'products': [
            {
                'name': unicode,
                'quantity': int,
                'weight': float,
            }
        ],
        'estimated_delivery_date': datetime,
        'carrier': unicode,
        'driver': unicode,
        'last_updated': datetime,
    }
    required_fields = ['order_id', 'customer_name', 'status']
    default_values = {'last_updated': datetime.now}

    ### Step 5: Initialize the document instance (using 'mongokit')

    meta = {
        'collection': orders_collection,
        'indexes': [
            {'fields': ['order_id'], 'unique': True},
            {'fields': ['status', 'estimated_delivery_date']},
        ]
    }

    order1 = Order()

    ### Step 6: Data Abstraction Layer: (Encapsulating data storage and retrieval)
    @classmethod
    def create_order(cls, order_data):
        order = cls()
        order.update(order_data)
        order.save()
        return order

    @classmethod
    def get_order_by_id(cls, order_id):
        return cls.find_one({'order_id': order_id})

    @classmethod
    def update_order_status(cls, order_id, new_status):
        order = cls.get_order_by_id(order_id)
        if order:
            order.status = new_status
            order.last_updated = datetime.now()
            order.save()
        return order
