import os,json
import boto3
import uuid
from datetime import datetime
from pymongo import MongoClient
from bson import ObjectId

MONGO_URI  = os.environ["MONGO_URI"]
DB_NAME    = os.environ["MONGO_DB_NAME"]
COLLECTION = os.environ["MONGO_COLLECTION"]

# Reuse client across invocations (Lambda execution context reuse)
_client = MongoClient(MONGO_URI, tls=True)
_coll = _client[DB_NAME][COLLECTION]

def _resp(code, body):
    return {
        "statusCode": code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Methods": "GET,POST,OPTIONS",
        },
        "body": json.dumps(body, default=_json_default),
    }

def _json_default(o):
    if isinstance(o, ObjectId):
        return str(o)
    return o

def lambda_handler(event, _):
    method = event.get("httpMethod", "GET")
    path = event.get("path", "/")

    if method == "OPTIONS":
        return _resp(200, {"ok": True})

    # POST /expense  -> insert
    if method == "POST" and path.endswith("/expense"):
        try:
            body = json.loads(event.get("body", "{}"))
            for k in ("title", "amount", "date"):
                if body.get(k) in (None, ""):
                    return _resp(400, {"error": f"{k} is required"})
            res = _coll.insert_one({
                "title": body["title"],
                "amount": body["amount"],
                "date": body["date"],
            })
            return _resp(201, {"message": "Expense saved", "insertedId": res.inserted_id})
        except Exception as e:
            return _resp(500, {"error": str(e)})

    # GET /expense   -> list all
    if method == "GET" and path.endswith("/expense"):
        try:
            docs = list(_coll.find({}, {"_id": 0}))  # hide _id for simplicity
            return _resp(200, docs)
        except Exception as e:
            return _resp(500, {"error": str(e)})

    return _resp(404, {"error": "Not found"})
