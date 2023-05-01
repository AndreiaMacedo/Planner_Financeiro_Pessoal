from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = "mysecretkey"

conn = sqlite3.connect("database.db")
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT, password TEXT)")
conn.commit()
conn.close()


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, password))
        conn.commit()
        conn.close()
        return redirect("/login")
    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
        user = c.fetchone()
        conn.close()
        if user:
            session["user"] = user
            return redirect("/dashboard")
        else:
            error = "Invalid email or password"
            return render_template("login.html", error=error)
    return render_template("login.html")

@app.route("/dashboard", methods=['GET', 'POST'])
def dashboard():
    user = session.get("user")
    if not user:
        return redirect("/login")

    if request.method == 'POST':
        if 'cadastrar_despesa' in request.form:
            data_pagamento = request.form['data_pagamento']
            nome_despesa = request.form['nome_despesa']
            tipo_despesa = request.form['tipo_despesa']
            valor_despesa: float = request.form['valor_despesa']
            conn = sqlite3.connect('financeiro.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO despesas (data_pagamento, nome_despesa, tipo_despesa, valor_despesa) VALUES (?, ?, ?, ?)", (data_pagamento, nome_despesa, tipo_despesa, valor_despesa))
            conn.commit()
            conn.close()
            return redirect(url_for('dashboard'))

        elif 'cadastrar_receita' in request.form:
            data_recebimento = request.form['data_recebimento']
            nome_receita = request.form['nome_receita']
            tipo_receita = request.form['tipo_receita']
            valor_receita: float = request.form['valor_receita']
            conn = sqlite3.connect('financeiro.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO receitas (data_recebimento, nome_receita, tipo_receita, valor_receita) VALUES (?, ?, ?, ?)", (data_recebimento, nome_receita, tipo_receita, valor_receita))
            conn.commit()
            conn.close()
            return redirect(url_for('dashboard'))

    conn = sqlite3.connect('financeiro.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM despesas")
    despesas = cursor.fetchall()
    cursor.execute("SELECT * FROM receitas")
    receitas = cursor.fetchall()
    conn.close()

    return render_template("dashboard.html", user=user, despesas=despesas, receitas=receitas)

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")

if __name__ == "__main__":
    app.run(debug=True)
