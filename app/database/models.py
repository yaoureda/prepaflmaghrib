from .database import db
import enum
from sqlalchemy import Enum

class Filiere(enum.Enum):
    MP="MP"
    PC="PC"

class Matieres(enum.Enum):
    MATHS = "Maths"
    PHYSIQUE = "Physique"
    CHIMIE = "Chimie"
    SI = "SI"
    INFORMATIQUE = "Informatique"

class Annale(db.Model):
    __tablename__ = 'annales'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), nullable=False)
    filiere = db.Column(Enum(Filiere), nullable=False)
    matiere = db.Column(Enum(Matieres), nullable=False)
    annee = db.Column(db.Integer, nullable=False)
    themes = db.Column(db.String(100), nullable=False)
    corrige = db.Column(db.String(255), nullable=False)

    def to_dict(self):
        return {
            'url': self.url,
            'filiere': self.filiere.value,
            'matiere': self.matiere.value,
            'annee': self.annee,
            'themes': self.themes,
            'corrige': self.corrige
        }