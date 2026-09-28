import os
import time

import psycopg2
from flask import Flask, redirect, render_template_string, request, url_for

app = Flask(__name__)

DATABASE_URL = os.environ.get("DATABASE_URL")

PAGE = """
<!doctype html>
<html lang="pt-br">
<head>
  <meta charset="utf-8">
  <title>Lista de Tarefas</title>
  <style>
    body { font-family: Arial, sans-serif; max-width: 560px; margin: 40px auto; padding: 0 16px; }
    h1 { font-size: 1.5rem; }
    form { display: flex; gap: 8px; margin-bottom: 24px; }
    input[type=text] { flex: 1; padding: 8px; }
    button { padding: 8px 16px; }
    ul { list-style: none; padding: 0; }
    li { padding: 8px; border-bottom: 1px solid #ddd; }
  </style>
</head>
<body>
  <h1>Lista de Tarefas</h1>
  <form method="post" action="{{ url_for('criar_tarefa') }}">
    <input type="text" name="titulo" placeholder="Nova tarefa" required>
    <button type="submit">Adicionar</button>
  </form>
  <ul>
    {% for tarefa in tarefas %}
      <li>#{{ tarefa[0] }} — {{ tarefa[1] }}</li>
    {% else %}
      <li>Nenhuma tarefa cadastrada ainda.</li>
    {% endfor %}
  </ul>
</body>
</html>
"""


def get_conn():
    return psycopg2.connect(DATABASE_URL)


def init_db(retries=10, delay=2):
    """Cria a tabela de tarefas caso ainda não exista.

    O healthcheck do banco no docker-compose já garante que o serviço
    'db' está pronto antes deste container subir, mas mantemos um
    pequeno retry aqui como segurança extra.
    """
    last_error = None
    for _ in range(retries):
        try:
            conn = get_conn()
            cur = conn.cursor()
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS tarefas (
                    id SERIAL PRIMARY KEY,
                    titulo TEXT NOT NULL,
                    criada_em TIMESTAMP NOT NULL DEFAULT NOW()
                );
                """
            )
            conn.commit()
            cur.close()
            conn.close()
            return
        except psycopg2.OperationalError as exc:
            last_error = exc
            time.sleep(delay)
    raise RuntimeError(f"Não foi possível conectar ao banco: {last_error}")


@app.route("/")
def listar_tarefas():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, titulo FROM tarefas ORDER BY id;")
    tarefas = cur.fetchall()
    cur.close()
    conn.close()
    return render_template_string(PAGE, tarefas=tarefas)


@app.route("/tasks", methods=["POST"])
def criar_tarefa():
    titulo = request.form.get("titulo", "").strip()
    if titulo:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("INSERT INTO tarefas (titulo) VALUES (%s);", (titulo,))
        conn.commit()
        cur.close()
        conn.close()
    return redirect(url_for("listar_tarefas"))


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
