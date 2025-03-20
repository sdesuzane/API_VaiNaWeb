from flask import Flask, request, jsonify  # Importamos a classe Flask do módulo flask para criar nosso aplicativo web
import sqlite3

# Aqui estamos criando uma instância do Flask e armazenando na variável "app"
# O parâmetro __name__ é passado para o Flask para que ele consiga identificar o arquivo principal da aplicação
app = Flask(__name__)

# Aqui estamos criando uma rota para o endpoint "/pagar"
# Ou seja, quando acessarmos http://127.0.0.1:5000/pagar no navegador, a função abaixo será executada
@app.route("/pagar")
def exibir_mensagem():
    # Retorna um texto formatado em HTML para ser exibido na página da rota "/pagar"
    return "<h1>Pagar as pessoas, faz bem as pessoas!!!</h1>"

# Criamos outra rota para o endpoint "/femandaopix"
# Quando acessarmos http://127.0.0.1:5000/femandaopix, a função será chamada automaticamente
@app.route("/femandaopix")
def manda_o_pix():
    # Retorna um texto formatado em HTML que será exibido no navegador
    return "<h2>SE TEM DOR DE CUTUVELO, TÁ DEVENDO</h2>"

# Criamos uma terceira rota para o endpoint "/comida"
# Sempre que o usuário acessar http://127.0.0.1:5000/comida, essa função será executada
@app.route("/comida")
def comida():
    # Retorna um texto formatado em HTML com uma mensagem sobre comida
    return "<h2>Tomato à milanesa</h2>"

# iniciando o banco de dados
def init_db():
    # criando o banco de dados com o arquivo 'database.db' e conectando a variavel 'conn' --> (responsavel por comunicar tudo que quer fazer no banco de dados)
    with sqlite3.connect("database.db") as conn:
        # executando um comando SQL para criar uma tabela chamada 'LIVROS'
        # IF NOT EXISTS é uma cláusula que verifica se a tabela já existe, caso exista, não será criada novamente
        conn.execute(
            """
                CREATE TABLE IF NOT EXISTS LIVROS (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    titulo TEXT NOT NULL,
                    categoria TEXT NOT NULL,
                    autor TEXT NOT NULL,
                    imagem_url TEXT NOT NULL
                )
            """
        )
init_db()

@app.route("/doar", methods=["POST"])
def doar():
    dados = request.get_json()
    print(f"Aqui estão os dados: {dados}")

    titulo = dados.get("titulo")
    categoria = dados.get("categoria")
    autor = dados.get("autor")
    imagem_url = dados.get("imagem_url")


    if not titulo or not categoria or not autor or not imagem_url:
        return jsonify({"erro": "Todos os campos sao obrigatorios"}), 400

    with sqlite3.connect("database.db") as conn:

        conn.execute(
            """
                INSERT INTO LIVROS (titulo, categoria, autor, imagem_url)
                VALUES (?, ?, ?, ?)
            """,
            (titulo, categoria, autor, imagem_url)
        )

    conn.commit() # Salva as alterações no banco de dados


    return jsonify({"mensagem": "Livro cadastrado com sucesso"}), 201


# Aqui verificamos se o script está sendo executado diretamente e não importado como módulo
if __name__ == "__main__":
    # Inicia o servidor Flask no modo de depuração
    # O modo debug faz com que as mudanças no código sejam aplicadas automaticamente, sem necessidade de reiniciar o servidor manualmente
    app.run(debug=True)
