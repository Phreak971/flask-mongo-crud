from flask import Flask, request, json, Response
from pymongo import MongoClient, collection, response

class MongoAPI:
    def __init__(self, data):
        self.client = MongoClient("mongodb://localhost:5000/")  # When only Mongo DB is running on Docker.
        #self.client = MongoClient("mongodb://mymongo_1:27017/")     # When both Mongo and This application is running on
                                                                    # Docker and we are using Docker Compose

        database = data['database']
        collection = data['collection']
        cursor = self.client[database]
        self.collection = cursor[collection]
        self.data = data

    def read(self):
        documents = self.collection.find()
        output = [{item: data[item] for item in data if item != '_id'} for data in documents]
        return output

    def write(self, data):
        new_document = data['Document']
        response = self.collection.insert_one(new_document)
        output = {'Status': 'Successfully Inserted',
                  'Document_ID': str(response.inserted_id)}
        return output

    def update(self):
        filt = self.data['Filter']
        updated_data = {"$set": self.data['DataToBeUpdated']}
        response = self.collection.update_one(filt, updated_data)
        output = {'Status': 'Successfully Updated' if response.modified_count > 0 else "Nothing was updated."}
        return output

    def delete(self, data):
        filt = data['Filter']
        response = self.collection.delete_one(filt)
        output = {'Status': 'Successfully Deleted' if response.deleted_count > 0 else "Document not found."}
        return output

if __name__ == '__main__':
    data = {
        "database": "mytestDB",
        "collection": "students",
    }
    mongo_obj = MongoAPI(data)
    print(json.dumps(mongo_obj.read(), indent=4))