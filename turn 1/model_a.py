import pymongo
from abc import ABC, abstractmethod


# Data Abstraction Layer Base Class
class LogisticsDataLayer(ABC):
    @abstractmethod
    def save_shipment(self, shipment_data):
        pass

    @abstractmethod
    def get_shipment(self, shipment_id):
        pass

    @abstractmethod
    def update_shipment_status(self, shipment_id, status):
        pass


# Concrete Implementation using MongoDB via Pymongo
class MongoLogisticsDataLayer(LogisticsDataLayer):
    def __init__(self, db_name, collection_name):
        self.client = pymongo.MongoClient('mongodb+srv://salimao:nwaJx9prHGPzS4dM@turing.h9o7m.mongodb.net/?retryWrites=true&w=majority&appName=turing')
        self.database = self.client[db_name]
        self.collection = self.database[collection_name]

    def save_shipment(self, shipment_data):
        self.collection.insert_one(shipment_data)

    def get_shipment(self, shipment_id):
        return self.collection.find_one({'_id': shipment_id})

    def update_shipment_status(self, shipment_id, status):
        self.collection.update_one({'_id': shipment_id}, {'$set': {'status': status}})


if __name__ == "__main__":
    # Usage example:
    import time

    # Using the Data Abstraction Layer
    data_layer = MongoLogisticsDataLayer(db_name="logistics", collection_name="shipments")

    # Simulate saving shipments
    shipment1 = {
        "_id": " shipment_id_1",
        "order_id": "order_1",
        "status": "Pending",
        "location": "Origin Hub",
        "destination": "Destination Warehouse",
        "items": ["productA", "productB"]
    }

    start_time = time.time()
    for _ in range(1000):
        data_layer.save_shipment(shipment1)
    print(f"Time taken to save 1000 shipments: {time.time() - start_time} seconds")

    # Simulate updating shipment status
    shipment_id_to_update = "shipment_id_1"
    new_status = "In Transit"
    data_layer.update_shipment_status(shipment_id_to_update, new_status)

    # Simulate fetching a shipment
    fetched_shipment = data_layer.get_shipment(shipment_id_to_update)
    print("Fetched Shipment:", fetched_shipment)
