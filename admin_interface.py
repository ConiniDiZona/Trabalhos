import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import mysql.connector

# Função para conectar ao banco de dados MySQL
def connect_db():
    return mysql.connector.connect(
        host="localhost",          # Ou o IP do servidor MySQL
        user="root",               # Seu usuário do MySQL
        password="2626",           # Sua senha do MySQL
        database="biblioteca"      # Nome do banco de dados
    )

# Função para carregar os livros
def load_books():
    for row in book_treeview.get_children():
        book_treeview.delete(row)
    
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM livros")
    books = cursor.fetchall()
    conn.close()
    
    for book in books:
        book_treeview.insert("", "end", values=book)

# Função para carregar os empréstimos
def load_borrowings():
    for row in borrow_treeview.get_children():
        borrow_treeview.delete(row)
    
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, NomeUser, NomeLivro, data_emprestimo, status FROM emprestimos WHERE status != 'Disponível'")
    borrowings = cursor.fetchall()
    conn.close()
    
    for borrow in borrowings:
        borrow_treeview.insert("", "end", values=borrow)


# Função para carregar os usuários
def load_users():
    for row in user_treeview.get_children():
        user_treeview.delete(row)
    
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios")
    users = cursor.fetchall()
    conn.close()
    
    for user in users:
        user_treeview.insert("", "end", values=user)

# Função para devolução do livro
def return_book():
    selected_item = borrow_treeview.selection()
    if selected_item:
        borrow_id = borrow_treeview.item(selected_item)['values'][0]  # ID do empréstimo
        conn = connect_db()
        cursor = conn.cursor()
        
        # Atualizar o status para 'Disponível' e definir a data de devolução
        cursor.execute("""
            UPDATE emprestimos
            SET status = 'Disponível', data_devolucao = NOW()
            WHERE id = %s
        """, (borrow_id,))
        
        conn.commit()
        conn.close()
        
        messagebox.showinfo("Success", "Empréstimo devolvido com sucesso!")
        load_borrowings()  # Recarregar a lista de empréstimos
    else:
        messagebox.showwarning("Selection Error", "Selecione um empréstimo para devolver!")

# Função para exibir o botão de devolução ao selecionar um item
def on_select_borrowing(event):
    selected_item = borrow_treeview.selection()
    if selected_item:
        return_button.grid(row=1, column=0, columnspan=2)  # Exibir o botão
    else:
        return_button.grid_forget()  # Esconder o botão quando nada estiver selecionado

# Função para adicionar um livro
def add_book():
    title = book_title_entry.get()
    author = book_author_entry.get()
    if title and author:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO livros (titulo, autor) VALUES (%s, %s)", (title, author))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Livro adicionado com sucesso")
        load_books()
    else:
        messagebox.showwarning("Input Error", "Preencha todos os campos!")

# Função para remover um livro
def remove_book():
    selected_item = book_treeview.selection()
    if selected_item:
        book_id = book_treeview.item(selected_item)['values'][0]
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM livros WHERE id = %s", (book_id,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Livro removido com sucesso")
        load_books()
    else:
        messagebox.showwarning("Selection Error", "Selecione um livro para remover!")

# Criação da janela principal
root = tk.Tk()
root.title("Interface Administrativa - Biblioteca")

# Abas
notebook = ttk.Notebook(root)
notebook.pack(pady=10)

# Aba de Livros
book_frame = ttk.Frame(notebook)
notebook.add(book_frame, text="Gerenciar Livros")

book_title_label = ttk.Label(book_frame, text="Título do Livro")
book_title_label.grid(row=0, column=0)
book_title_entry = ttk.Entry(book_frame)
book_title_entry.grid(row=0, column=1)

book_author_label = ttk.Label(book_frame, text="Autor")
book_author_label.grid(row=1, column=0)
book_author_entry = ttk.Entry(book_frame)
book_author_entry.grid(row=1, column=1)

add_book_button = ttk.Button(book_frame, text="Adicionar Livro", command=add_book)
add_book_button.grid(row=2, column=0, columnspan=2)

remove_book_button = ttk.Button(book_frame, text="Remover Livro", command=remove_book)
remove_book_button.grid(row=3, column=0, columnspan=2)

# Treeview de livros
book_treeview = ttk.Treeview(book_frame, columns=("ID", "Título", "Autor"), show="headings")
book_treeview.grid(row=4, column=0, columnspan=2)
book_treeview.heading("ID", text="ID")
book_treeview.heading("Título", text="Título")
book_treeview.heading("Autor", text="Autor")

# Carregar livros ao iniciar
load_books()

# Aba de Empréstimos
borrow_frame = ttk.Frame(notebook)
notebook.add(borrow_frame, text="Empréstimos")

# Treeview de empréstimos
borrow_treeview = ttk.Treeview(borrow_frame, columns=("ID", "Nome Usuário", "Nome Livro", "Data Empréstimo", "Status"), show="headings")
borrow_treeview.grid(row=0, column=0, columnspan=2)
borrow_treeview.heading("ID", text="ID")
borrow_treeview.heading("Nome Usuário", text="Nome Usuário")
borrow_treeview.heading("Nome Livro", text="Nome Livro")
borrow_treeview.heading("Data Empréstimo", text="Data Empréstimo")
borrow_treeview.heading("Status", text="Status")

# Carregar empréstimos ao iniciar
load_borrowings()

# Adicionar o botão para devolução do livro
return_button = ttk.Button(borrow_frame, text="Confirmar Devolução", command=return_book)
return_button.grid(row=1, column=0, columnspan=2)
return_button.grid_forget()  # Inicialmente esconder o botão

# Ligar o evento de seleção de uma linha para mostrar o botão
borrow_treeview.bind('<<TreeviewSelect>>', on_select_borrowing)

# Aba de Usuários
user_frame = ttk.Frame(notebook)
notebook.add(user_frame, text="Gerenciar Usuários")

# Treeview de usuários
user_treeview = ttk.Treeview(user_frame, columns=("ID", "Nome", "Email"), show="headings")
user_treeview.grid(row=0, column=0, columnspan=2)
user_treeview.heading("ID", text="ID")
user_treeview.heading("Nome", text="Nome")
user_treeview.heading("Email", text="Email")

# Carregar usuários ao iniciar
load_users()

# Atualizar a tabela de livros a cada 5 segundos
def update_tables():
    load_books()
    load_borrowings()
    load_users()
    root.after(5000, update_tables)  # Chama a função novamente após 5 segundos (5000 ms)

# Chama a função de atualização inicial
update_tables()

root.mainloop()
