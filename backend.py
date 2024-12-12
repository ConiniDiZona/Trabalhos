from flask import Flask, request, jsonify
from flask_restful import Api, Resource
import pymysql
from pymongo import MongoClient
from flask_cors import CORS
import requests
import jwt
from datetime import datetime, timedelta
import bcrypt

# Inicialização do app Flask
app = Flask(__name__)
CORS(app)
api = Api(app)

SECRET_KEY = "sua_chave_secreta"

# Configuração do MySQL
mysql_connection = pymysql.connect(
    host="localhost",
    user="root",
    password="2626",
    database="biblioteca"
)

# Configuração do MongoDB para logs de ações
mongo_client = MongoClient("mongodb://localhost:27017/")
mongo_db = mongo_client["biblioteca_logs"]
user_logs = mongo_db["user_logs"]

# Rota para listar todos os livros
class Books(Resource):
    def get(self):
        try:
            cursor = mysql_connection.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT id, titulo AS title, autor AS author FROM livros")
            books = cursor.fetchall()
            return jsonify(books)
        except Exception as e:
            return jsonify({"error": str(e)})

# Rota para registrar um empréstimo
class Borrow(Resource):
    def post(self):
        try:
            data = request.get_json()
            book_id = data.get("book_id")
            user_token = request.headers.get("Authorization")
            
            if not user_token:
                return {"error": "Token não fornecido"}, 403

            # Decodificar o token JWT
            try:
                token = user_token.split(" ")[1]  # Remove o "Bearer " do token
                decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
                user_id = decoded["user_id"]
            except jwt.ExpiredSignatureError:
                return {"error": "Token expirado"}, 403
            except jwt.InvalidTokenError:
                return {"error": "Token inválido"}, 403

            if not book_id:
                return {"error": "book_id é obrigatório"}, 400

            # Verificar se o livro já existe na tabela de livros
            cursor = mysql_connection.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT id FROM livros WHERE google_books_id = %s", (book_id,))
            existing_book = cursor.fetchone()

            if not existing_book:
                # Se o livro não existe, adicionar o livro à tabela 'livros'
                cursor.execute(
                    "INSERT INTO livros (google_books_id) VALUES (%s)",
                    (book_id,)  # Apenas inserimos o ID do livro da API
                )
                mysql_connection.commit()

            # Recuperar o nome do usuário logado
            cursor.execute("SELECT nome FROM usuarios WHERE id = %s", (user_id,))
            user = cursor.fetchone()

            if not user:
                return {"error": "Usuário não encontrado"}, 404

            NomeUser = user["nome"]

            # Agora vamos buscar o título diretamente da API usando o book_id
            api_url = f"https://www.googleapis.com/books/v1/volumes/{book_id}"  # URL da API para buscar o livro
            response = requests.get(api_url)
            if response.status_code != 200:
                return {"error": "Erro ao buscar dados do livro na API"}, 500
            
            book_data = response.json()
            NomeLivro = book_data['volumeInfo']['title']  # Título do livro vindo da API

            # Registrar o empréstimo na tabela
            cursor.execute(
                "INSERT INTO emprestimos (NomeUser, NomeLivro, data_emprestimo) VALUES (%s, %s, NOW())",
                (NomeUser, NomeLivro)
            )
            mysql_connection.commit()

            return {"message": "Empréstimo realizado com sucesso"}, 201

        except Exception as e:
            return {"error": f"Erro inesperado: {str(e)}"}, 500

# Rota para devolver um livro
class Return(Resource):
    def put(self):
        try:
            data = request.get_json()
            cursor = mysql_connection.cursor()
            cursor.execute(
                "UPDATE emprestimos SET data_devolucao = NOW(), status = 'devolvido' WHERE id = %s",
                (data['emprestimo_id'],)
            )
            mysql_connection.commit()
            user_logs.insert_one({
                "users_id": data['user_id'],
                "action": "return",
                "emprestimo_id": data['emprestimo_id']
            })
            return jsonify({"message": "Devolução realizada com sucesso"})
        except Exception as e:
            return jsonify({"error": str(e)})

# Integração com a Google Books API
class GoogleBooks(Resource):
    def get(self):
        query = request.args.get('q')
        if not query:
            return jsonify({"error": "Parâmetro de consulta é obrigatório"})
        
        google_books_api_url = f"https://www.googleapis.com/books/v1/volumes?q={query}&key=AIzaSyC_3oJz8V3fA3vITgH3R8sMjsXLbt6Ctf0"
        try:
            response = requests.get(google_books_api_url)
            response.raise_for_status()
            books_data = response.json()
            return jsonify(books_data)
        except requests.exceptions.RequestException as e:
            return jsonify({"error": str(e)})


# Rota para adicionar livros na base de dados
class AddBook(Resource):
    def post(self):
        try:
            data = request.get_json()
            cursor = mysql_connection.cursor()
            sql_query = (
                "INSERT INTO livros (titulo, autor, ano_publicacao, genero, google_books_id) "
                "VALUES (%s, %s, %s, %s, %s)"
            )
            values = (
                data['title'],
                ', '.join(data.get('authors', [])),
                data.get('publishedDate', '').split('-')[0],
                data.get('categories', ['Desconhecido'])[0],
                data['google_books_id']
            )
            cursor.execute(sql_query, values)
            mysql_connection.commit()
            return jsonify({"message": "Livro adicionado com sucesso"})
        except Exception as e:
            return jsonify({"error": str(e)})
        
class Register(Resource):
    def post(self):
        try:
            data = request.get_json()
            nome = data.get("nome")
            email = data.get("email")
            senha = data.get("senha")

            # Verificar se todos os campos estão preenchidos
            if not all([nome, email, senha]):
                return {"error": "Todos os campos são obrigatórios"}, 400

            # Verificar se o email já existe
            cursor = mysql_connection.cursor()
            cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
            if cursor.fetchone():
                return {"error": "Email já está em uso"}, 400

            # Hashear a senha
            hashed_senha = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())

            # Inserir o usuário na tabela
            cursor.execute(
                "INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s)",
                (nome, email, hashed_senha.decode('utf-8'))
            )
            mysql_connection.commit()

            return {"message": "Usuário registrado com sucesso"}, 201

        except pymysql.MySQLError as e:
            # Registrar erros específicos do MySQL
            print(f"Erro MySQL: {str(e)}")
            return {"error": f"Erro no banco de dados: {str(e)}"}, 500
        except Exception as e:
            # Registrar erros inesperados
            print(f"Erro inesperado: {str(e)}")
            return {"error": f"Erro inesperado: {str(e)}"}, 500


        
class Login(Resource):
    def post(self):
        try:
            data = request.get_json()
            email = data.get("email")
            senha = data.get("senha")

            # Verificar se os campos estão preenchidos
            if not all([email, senha]):
                return {"error": "Email e senha são obrigatórios"}, 400

            # Buscar o usuário no banco de dados
            cursor = mysql_connection.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
            user = cursor.fetchone()

            if not user:
                return {"error": "Email não encontrado"}, 404

            # Verificar a senha
            if not bcrypt.checkpw(senha.encode('utf-8'), user['senha'].encode('utf-8')):
                return {"error": "Senha incorreta"}, 401

            # Gerar um token JWT
            token = jwt.encode(
                {
                    "user_id": user["id"],
                    "exp": datetime.utcnow() + timedelta(hours=1)
                },
                SECRET_KEY,
                algorithm="HS256"
            )

            return {
                "token": token,
                "nome": user["nome"],  # Enviar o nome do usuário junto com o token
            }, 200

        except pymysql.MySQLError as e:
            return {"error": f"Erro no banco de dados: {str(e)}"}, 500
        except Exception as e:
            return {"error": f"Erro inesperado: {str(e)}"}, 500


        
from functools import wraps

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"error": "Token não fornecido"}), 403

        try:
            # Decodificar o token JWT
            decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            request.user_id = decoded["user_id"]
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expirado"}), 403
        except jwt.InvalidTokenError:
            return jsonify({"error": "Token inválido"}), 403

        return f(*args, **kwargs)
    return decorated




# Registro de rotas na API
api.add_resource(Books, '/books')
api.add_resource(Borrow, '/emprestimos')
api.add_resource(Return, '/devolucao')
api.add_resource(GoogleBooks, '/buscar_livros')
api.add_resource(AddBook, '/adicionar_livro')
api.add_resource(Register, '/register')
api.add_resource(Login, '/login')


# Inicialização do servidor
if __name__ == '__main__':
    app.run(debug=True)