from flask import Flask, request
import requests
from urllib.parse import quote_plus
from config import API_TOKEN, VISION_TEMPERATURE, PRO_TEMPERATURE
import re
import base64
import os

app = Flask('app')

@app.route('/')
def hello_world():
  return '<h1>Hello, World!</h1>'

@app.route('/gemini/vision')
def vision():
 url = request.args.get('url') 
 prompt = request.args.get('prompt')
 response = requests.get(url)
 return { "answer": get_pro_llm_response(response.content, prompt) }

def get_pro_llm_response(img,prompt):

    base64_img = base64.b64encode(img).decode("utf-8");

    data = {
    "contents": [
        {
            "parts": [
                {
                    "inlineData": {
                        "mimeType": "image/jpeg",
                        "data": base64_img
                    }
                },
                {"text":prompt},

            ]
        }
    ],
    "generationConfig": {
        "temperature": VISION_TEMPERATURE,
        "topK": 32,
        "topP": 1,
        "maxOutputTokens": 4096,
        "stopSequences": []
    },
    "safetySettings": [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        }
        ]
    }
    headers = {"Content-Type":"application/json"}
    url = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro-vision:generateContent?key=' + API_TOKEN
    response = requests.post(url, json=data, headers=headers)
    print(response.json())
    return response.json()['candidates'][0]['content']['parts'][0]['text'];

app.run(host='0.0.0.0', port=8080)
