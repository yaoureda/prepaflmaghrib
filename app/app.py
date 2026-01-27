from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from .database.database import db, init_database
from .database.models import Annale, Filiere, Matieres
from sqlalchemy import asc, desc
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-only-key')
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(basedir, 'database', 'database.db')}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app) 

with app.app_context():
    init_database()

@app.route("/")
def accueil():
    return render_template("accueil.html")

@app.route("/annales")
def annales():
    return render_template(
        "annales.html",
        filieres= Filiere,
        matieres= Matieres
    )

@app.route("/reussir")
def reussir():
    return render_template("reussir.html")

@app.route("/contacts")
def contacts():
    return render_template("contacts.html")

@app.route('/browse/annales', methods=['GET'])
def browse_annales():

    mots = request.args.get('mots')
    matiere = request.args.get('matiere')
    order = request.args.get('ordre_par_annee', 'desc')

    annales_query = Annale.query

    if mots:
        annales_query = annales_query.filter(Annale.themes.like(f'%{mots}%'))

    if matiere:
        annales_query = annales_query.filter_by(matiere=Matieres[matiere])

    if order == 'asc':
        annales_query = annales_query.order_by(Annale.annee.asc())
    else:
        annales_query = annales_query.order_by(Annale.annee.desc())

    annales = annales_query.all()
    return jsonify([a.to_dict() for a in annales])


if __name__ == "__main__":
    app.run(debug=False)