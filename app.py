from flask import Flask, jsonify, request, redirect
from pymongo import MongoClient, errors as PyMongoError
# from bson import ObjectId
from dotenv import load_dotenv
import os
from flask_cors import CORS
from datetime import datetime

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
        # Check if the email already exists in the database
        existing_subscriber = collection.find_one({'email': email})
        
        if existing_subscriber:
            if existing_subscriber['option'] == option:
                return jsonify({'message': 'Already subscribed'}), 200
            else:
                # Update the option and last_changed for the existing email
                result = collection.update_one(
                    {'email': email},
                    {
                        '$set': {'option': option, 'last_changed': datetime.utcnow()}
                    }
                )
                
                if result.modified_count > 0:
                    return jsonify({'message': 'Updated'}), 200
                else:
                    return jsonify({'error': 'Failed to update subscription'}), 500
        else:
            result = collection.insert_one({
                'email': email,
                'option': option,
                'created': datetime.utcnow(),
                'last_changed': datetime.utcnow()
            })
            
            if result.inserted_id:
                return jsonify({'message': 'Success', 'id': str(result.inserted_id)}), 201
            else:
                return jsonify({'error': 'Failed'}), 500
                
    except PyMongoError as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host="0.0.0.0",port=5000)