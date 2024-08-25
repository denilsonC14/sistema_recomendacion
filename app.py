import redis
import requests
from flask import Flask, request, jsonify

# Conectar a Redis
r = redis.Redis(host='localhost', port=6379, db=0)

app = Flask(__name__)

# Obtener datos de smartphones de la API de DummyJSON
def get_smartphones():
    url = "https://dummyjson.com/products/category/smartphones"
    response = requests.get(url)
    data = response.json()
    return data['products']

# Procesar los datos de smartphones y almacenarlos en Redis
def store_smartphones_in_redis(smartphones):
    for phone in smartphones:
        r.set(f"phone:{phone['id']}", phone['title'])

# Implementar un algoritmo de recomendación simple
def recommend_phones(input_text):
    recommendations = []
    for key in r.keys("phone:*"):
        title = r.get(key).decode('utf-8')
        if input_text.lower() in title.lower():
            recommendations.append(title)
    return recommendations

@app.route('/recommend', methods=['POST'])
def get_recommendations():
    data = request.get_json()
    input_text = data['input_text']
    recommendations = recommend_phones(input_text)
    return jsonify(recommendations)

if __name__ == '__main__':
    # Obtener y almacenar smartphones al iniciar la aplicación
    smartphones = get_smartphones()
    store_smartphones_in_redis(smartphones)
    app.run(debug=True)