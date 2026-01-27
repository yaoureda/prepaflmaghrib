from pathlib import Path
from flask import json
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_database():
    db.create_all()
    populate_database()

def populate_database():
    from .models import Annale, Filiere, Matieres

    BASE_DIR = Path(__file__).resolve().parent
    ANNALS_DIR = BASE_DIR / "annales"

    for json_file in ANNALS_DIR.glob("*.json"):
        with open(json_file, "r", encoding="utf-8") as f:
            annales = json.load(f)

        for data in annales:

            annale_exists = Annale.query.filter_by(
                filiere=Filiere[data["filiere"]],
                matiere=Matieres[data["matiere"]],
                annee=data["annee"],
                themes=data["themes"]
            ).first()

            if annale_exists:
                continue

            annale = Annale(
                url=data["url"],
                filiere=Filiere[data["filiere"]],
                matiere=Matieres[data["matiere"]],
                annee=data["annee"],
                themes=data["themes"],
                corrige=data["corrige"]
            )
            db.session.add(annale)

    db.session.commit()