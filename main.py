from flask import Flask, jsonify, request, send_from_directory
import os
import requests
from waitress import serve


# Initialize the Flask app
app = Flask(__name__)

# Read Pexels API key from environment variable
my_secret = os.environ['PEXELS_API_KEY']
PEXELS_BASE_URL = "https://api.pexels.com/v1/search"

@app.route('/')
def landing():
    return "Welcome to the Pexels API integration!"

@app.route('/v1/search', methods=['GET'])
def search_photos():
    query = request.args.get('query', '')
    orientation = request.args.get('orientation', '')
    size = request.args.get('size', '')
    color = request.args.get('color', '')
    locale = request.args.get('locale', '')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 15))

    headers = {
        "Authorization": my_secret  
    }

    params = {
        "query": query,
        "orientation": orientation,
        "size": size,
        "color": color,
        "locale": locale,
        "page": page,
        "per_page": per_page
    }

    try:
        response = requests.get(PEXELS_BASE_URL, headers=headers, params=params)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.route('/.well-known/ai-plugin.json')
def serve_ai_plugin():
  return send_from_directory('.',
                             'ai-plugin.json',
                             mimetype='application/json')


@app.route('/.well-known/openapi.yaml')
def serve_openapi_yaml():
  return send_from_directory('.', 'openapi.yaml', mimetype='text/yaml')

# Serve logo
@app.route('/pexels.png')
def plugin_logo():
  return send_from_directory('.', 'pexels.png')


if __name__ == '__main__':
  serve(app, host="0.0.0.0", port=8080)
