from flask import Flask, jsonify, request, redirect
from pymongo import MongoClient, errors as PyMongoError
# from bson import ObjectId
from dotenv import load_dotenv
import os
from flask_cors import CORS

load_dotenv()
app = Flask(__name__)

CORS(app)

host = os.environ["DB_HOST"]
password = os.environ["DB_PASS"]

mongodb_uri = f"mongodb+srv://{host}:{password}@cluster0.gurdfx8.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(mongodb_uri)
db = client["NW"]

collection = db["Subs"]

@app.route('/')
def index():
    return redirect("https://northernwhisper.tech", code=302)

@app.route('/api/subscribe', methods=['POST'])
def subscribe():
    data = request.json
    email = data.get('email')
    option = data.get('option')
    
    if not email or not option:
        return jsonify({'error': 'Email and option are required'}), 400
    
    try:
        # Save data to MongoDB
        result = collection.insert_one({'email': email, 'option': option})
        
        # Check if the data was inserted successfully
        if result.inserted_id:
            return jsonify({'message': 'Subscription successful', 'id': str(result.inserted_id)}), 201
        else:
            return jsonify({'error': 'Failed to insert data'}), 500
    except PyMongoError as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host="0.0.0.0",port=5000)