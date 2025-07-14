import data_wizard
from .models import Diakon, Mitarbeiter, Kontakt, Dokument, Beurteilung, Einsatzort, Einsatz

data_wizard.register(
    Diakon,
)