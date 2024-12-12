from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split
from surprise import accuracy
import pandas as pd

# Dados de exemplo (você pode substituir pelos dados do seu banco de dados)
data = {
    'user_id': [1, 2, 3, 1, 2, 3],
    'book_id': [101, 102, 103, 104, 105, 106],
    'rating': [5, 4, 3, 4, 5, 4]
}

df = pd.DataFrame(data)

# Defina o formato dos dados para o surprise
reader = Reader(rating_scale=(1, 5))
data = Dataset.load_from_df(df[['user_id', 'book_id', 'rating']], reader)

# Divida os dados em conjunto de treinamento e teste
trainset, testset = train_test_split(data, test_size=0.2)

# Usando o algoritmo SVD (Singular Value Decomposition)
model = SVD()

# Treinar o modelo
model.fit(trainset)

# Testar o modelo
predictions = model.test(testset)
print("Root Mean Squared Error (RMSE): ", accuracy.rmse(predictions))

# Função para gerar recomendações
def get_recommendations(user_id, top_n=5):
    # Obtenha os livros que o usuário já interagiu
    user_books = df[df['user_id'] == user_id]['book_id'].tolist()

    # Recomenda livros que o usuário ainda não interagiu
    all_books = df['book_id'].unique().tolist()
    books_to_predict = [book for book in all_books if book not in user_books]
    
    predictions = []
    for book in books_to_predict:
        pred = model.predict(user_id, book)
        predictions.append(pred)
    
    # Ordene as previsões e retorne os top N livros recomendados
    predictions.sort(key=lambda x: x.est, reverse=True)
    recommended_books = [pred.iid for pred in predictions[:top_n]]
    
    return recommended_books
