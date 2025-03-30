from flask import Flask, request, jsonify
import sqlite3
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


@app.route("/")
def manda_o_pix():
    return "<h2>SE TEM DOR DE CUTUVELO, TÁ DEVENDO</h2>"


def init_db():
    with sqlite3.connect("database.db") as conn:
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

        conn.execute(f"""
                INSERT INTO LIVROS (titulo, categoria, autor, imagem_url)
                VALUES ("{titulo}", "{categoria}", "{autor}", "{imagem_url}")
            """)

    conn.commit()


    return jsonify({"mensagem": "Livro cadastrado com sucesso"}), 201


@app.route("/livros", methods=["GET"])
def listar_livros():
    with sqlite3.connect("database.db") as conn:
        livros = conn.execute("SELECT * FROM LIVROS").fetchall()
        lista_formatados = []
        for item in livros:
            dicionario_livros = {
                "id": item[0],
                "titulo": item[1],
                "categoria": item[2],
                "autor": item[3],
                "imagem_url": item[4]
            }

            lista_formatados.append(dicionario_livros)

            
    return jsonify(lista_formatados), 200


if __name__ == "__main__":
    app.run(debug=True)
