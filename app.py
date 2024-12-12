from flask import Flask, jsonify, request
from recommendation_model import get_recommendations  # Importando a função de recomendação

app = Flask(__name__)

@app.route('/recommendations/<int:user_id>', methods=['GET'])
def recommend_books(user_id):
    top_n = int(request.args.get('top_n', 5))  # Número de recomendações (default 5)
    
    # Obtenha as recomendações
    recommended_books = get_recommendations(user_id, top_n)
    
    return jsonify({'recommended_books': recommended_books})

if __name__ == '__main__':
    app.run(debug=True)
