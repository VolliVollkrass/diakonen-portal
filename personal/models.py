
from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.utils import timezone

# Optional: zur besseren Lesbarkeit
FAMILIENSTAND_CHOICES = [
    ('ledig', 'Ledig'),
    ('verheiratet', 'Verheiratet'),
    ('geschieden', 'Geschieden'),
    ('verwitwet', 'Verwitwet'),
]

KONTAKTART_CHOICES = [
    ('telefon', 'Telefon'),
    ('email', 'E-Mail'),
    ('persoenlich', 'Persönlich'),
    ('brief', 'Brief'),
]

KONTAKTGRUND_CHOICES = [
    ('allgemein', 'Allgemein'),
    ('versetzung', 'Versetzung'),
    ('teildienst', 'Teildienst'),
    ('beurlaubung', 'Beurlaubung'),
    ('beförderung', 'Beförderung'),
    ('krankheit', 'Krankheit'),
    ('fortbildung', 'Fortbildung'),
    ('ruhestand', 'Ruhestand'),
    ('besoldung', 'Besoldung'),
    ('rechtliches', 'Rechtliches'),
    ('problematik', 'Problematik'),
    ('sonstiges', 'Sonstiges'),
]

TRAEGER_CHOICES = [
    ('elkb', 'ELKB'),
    ('diak_traeger', 'Diakonischer Träger'),
    ('sonst_traeger', 'Sonstiger Träger'),
]

BEARBEITUNGSSTAND_CHOICES = [
    ('offen', 'Offen'),
    ('in_bearbeitung', 'In Bearbeitung'),
    ('erledigt', 'Erledigt'),
]
class Mitarbeiter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='mitarbeiter')
    name = models.CharField(max_length=100,null= True)
    email = models.CharField(max_length=30, unique=True)
    telefon = models.CharField(max_length=30,null=True)
    abteilung = models.CharField(max_length=100, null=True)
    ist_aktiv = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username}"

# Diakon-Stammdaten
class Diakon(models.Model):
    personalnummer = models.CharField(max_length=20, unique=True)
    geschlecht = models.CharField(max_length=10, choices=[('m', 'Männlich'), ('w', 'Weiblich'), ('d', 'Divers')])
    traeger = models.CharField(max_length=20, choices=TRAEGER_CHOICES, default='elkb')
    vorname = models.CharField(max_length=50)
    nachname = models.CharField(max_length=50)
    adresse = models.CharField(max_length=200, null=True)
    plz = models.CharField(max_length=10, null=True)
    ort = models.CharField(max_length=100, null=True)
    telefon = models.CharField(max_length=30, null=True, blank=True)
    mobil = models.CharField(max_length=30, null=True, blank=True)
    email = models.EmailField(max_length=100, unique=True)
    geburtsdatum = models.DateField()
    familienstand = models.CharField(max_length=20, choices=FAMILIENSTAND_CHOICES)
    kinder = models.PositiveIntegerField(default=0)
    besoldung = models.CharField(max_length=50)
    besoldungsstufe = models.CharField(max_length=10)
    innenauftragsnummer = models.CharField(max_length=50, blank=True, null=True)
    erstellt_am = models.DateTimeField(default=timezone.now)
    erstellt_durch = models.ForeignKey(Mitarbeiter, on_delete=models.SET_NULL, null=True, related_name='diakon_ersteller')
    aktualisiert_am = models.DateTimeField(blank=True, null=True)
    aktualisiert_durch = models.ForeignKey(Mitarbeiter, on_delete=models.SET_NULL, blank=True, null=True, related_name='diakon_aktualisierer')

    def __str__(self):
        return f"{self.vorname} {self.nachname} ({self.personalnummer})"
    
    def alter(self):
        today = date.today()
        return today.year - self.geburtsdatum.year - ((today.month, today.day) < (self.geburtsdatum.month, self.geburtsdatum.day))

    def aktualisiert_am(self):
        self.aktualisiert_am = timezone.now()
        self.save()

    @property
    def letzter_einsatz(self):
        """Gibt den letzten Einsatz des Diakons zurück."""
        return self.einsaetze.order_by('-startdatum').first() if self.einsaetze.exists() else None

# Kontakt / Telefonprotokoll
class Kontakt(models.Model):
    diakon = models.ForeignKey(Diakon, on_delete=models.SET_NULL, related_name='kontakte', null=True, blank=True)
    datum = models.DateField(auto_now_add=True)
    erfasser = models.ForeignKey(Mitarbeiter, on_delete=models.SET_NULL, null=True)
    kontaktart = models.CharField(max_length=20, choices=KONTAKTART_CHOICES, default='telefon')
    bearbeitungsstand = models.CharField(max_length=20, choices=BEARBEITUNGSSTAND_CHOICES, default='offen')
    kontaktgrund = models.CharField(max_length=20, choices=KONTAKTGRUND_CHOICES)
    kommentar = models.TextField()
    pk_ua = models.BooleanField(default=False, verbose_name="PK UA")
    pe = models.BooleanField(default=False, verbose_name="PE")

    def __str__(self):
        return f"{self.kontaktart.title()} am {self.datum} ({self.bearbeitungsstand})"

# Dokumente
class Dokument(models.Model):
    diakon = models.ForeignKey(Diakon, on_delete=models.CASCADE, related_name='dokumente')
    datei = models.FileField(upload_to='diakon_dokumente/{diakon.personalnummer}/')
    hochgeladen_am = models.DateTimeField(auto_now_add=True)
    beschreibung = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Dokument für {self.diakon} ({self.datei.name})"
    
class Beurteilung(models.Model):
    diakon = models.ForeignKey(Diakon, on_delete=models.SET_NULL, related_name='beurteilungen', null=True)
    datum = models.DateField()
    note = models.PositiveIntegerField(choices=[(i, str(i)) for i in range(1, 16)])
    beurteilende_person = models.CharField(max_length=50)

    def __str__(self):
        return f"Beurteilung {self.note} am {self.datum} durch {self.beurteilende_person}"
    
# Einsatzort
class Einsatzort(models.Model):
    standort_id = models.CharField(max_length=20, unique=True)
    traegername = models.CharField(max_length=100, blank=True, null=True)
    adresse = models.CharField(max_length=200, blank=True, null=True)
    plz = models.CharField(max_length=10, blank=True, null=True)
    ort = models.CharField(max_length=100, blank=True, null=True)
    telefon = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    fax = models.CharField(max_length=30, blank=True, null=True)
    traegerform = models.CharField(max_length=20, choices=TRAEGER_CHOICES, default='ELKB')

    @property
    def letzter_diakon(self):
        return self.einsaetze.order_by('-startdatum').first() if self.einsaetze.exists() else None
    
    def __str__(self):
        return f"{self.traegername} ({self.standort_id})"

# Einsatz
class Einsatz(models.Model):
    diakon = models.ForeignKey(Diakon, on_delete=models.CASCADE, related_name='einsaetze')
    einsatzbezeichnung = models.CharField(max_length=100, blank=True, null=True)
    einsatzort = models.ForeignKey(Einsatzort, on_delete=models.CASCADE)
    verantwortlicher = models.CharField(max_length=100, blank=True, null=True)
    startdatum = models.DateField()
    enddatum = models.DateField(null=True, blank=True)
    umfang = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.diakon} – {self.einsatzort} ({self.startdatum} bis {self.enddatum or 'offen'})"

class Pkua(models.Model):
    diakon = models.ForeignKey(Diakon, on_delete=models.CASCADE, blank=True, null=True, related_name='pkua_diakone')
    einsatz = models.ForeignKey(Einsatz, on_delete=models.CASCADE, related_name='pkua_einsaetze', null=True, blank=True)
    kontakt = models.ForeignKey(Kontakt, on_delete=models.CASCADE, related_name='pkua_kontakte', null=True, blank=True)
    datum_add = models.DateField(auto_now_add=True)
    besprochen_am = models.DateField(blank=True, null=True)
    besprochenes_thema = models.CharField(max_length=100, blank=True, null=True)
    beschluss = models.TextField(blank=True, null=True)
    erfasser = models.ForeignKey(Mitarbeiter, on_delete=models.SET_NULL, null=True, related_name='pkua_erfasser')
    pk_protokoll = models.BooleanField(default=False)

    def besprochen_am(self):
        self.besprochen_am = timezone.now()
        self.save()

    def __str__(self):
        return f"PK UA für {self.diakon} am {self.besprochen_am} ({self.besprochenes_thema})"
