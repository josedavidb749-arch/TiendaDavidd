from flask import Flask, render_template, request, redirect
import json
import os
app = Flask(__name__)
CARPETA = os.path.dirname(os.path.abspath(__file__))
ARCHIVO = os.path.join(CARPETA, "data", "videojuegos.json")

def leer():
    try:
        with open(ARCHIVO, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except:
        return []


def guardar(juegos):
    with open(ARCHIVO, "w", encoding="utf-8") as archivo:
        json.dump(juegos, archivo, indent=4, ensure_ascii=False)


@app.route("/")
def inicio():
    return render_template("inicio.html")


@app.route("/videojuegos")
def videojuegos():
    juegos = leer()
    return render_template("videojuegos.html", juegos=juegos)

@app.route("/precios")
def precios():
    juegos = leer()
    return render_template("precios.html", juegos=juegos)


@app.route("/registrar", methods=["GET", "POST"])
def registrar():
    if request.method == "POST":
        juegos = leer()
        nuevo = {
            "titulo": request.form["titulo"],
            "plataforma": request.form["plataforma"],
            "precio": request.form["precio"]
        }
        juegos.append(nuevo)
        guardar(juegos)
        return redirect("/videojuegos")
    return render_template("registrar.html")


@app.route("/editar/<int:n>", methods=["GET", "POST"])
def editar(n):
    juegos = leer()
    if n >= len(juegos):
        return redirect("/videojuegos")
    if request.method == "POST":
        juegos[n]["titulo"] = request.form["titulo"]
        juegos[n]["plataforma"] = request.form["plataforma"]
        juegos[n]["precio"] = request.form["precio"]
        guardar(juegos)
        return redirect("/videojuegos")
    return render_template("editar.html", juego=juegos[n], n=n)


@app.route("/eliminar/<int:n>")
def eliminar(n):
    juegos = leer()
    if n < len(juegos):
        juegos.pop(n)
        guardar(juegos)
    return redirect("/videojuegos")


@app.route("/informacion")
def informacion():
    return render_template("informacion.html")

if __name__ == "__main__":
    app.run(debug=True)