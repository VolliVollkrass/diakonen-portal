from django import forms
from .models import Kontakt, Diakon, Mitarbeiter, Einsatz, Einsatzort

class KontaktForm(forms.ModelForm):
    class Meta:
        model = Kontakt
        fields = ('kontaktart', 'kontaktgrund', 'kommentar', 'bearbeitungsstand', 'pk_ua', 'pe')

        widgets = {
            'kontaktart': forms.Select(attrs={'class': 'form-control'}),
            'bearbeitungsstand': forms.Select(attrs={'class': 'form-control'}),
            'kontaktgrund': forms.Select(attrs={'class': 'form-control'}),
            'kommentar': forms.Textarea(attrs={'class': 'form-control', 'rows': 7}),
            'pk_ua': forms.CheckboxInput(attrs={'class': 'form-check'}),
            'pe': forms.CheckboxInput(attrs={'class': 'form-check'}),
        }

class DiakonForm(forms.ModelForm):
    class Meta:
        model = Diakon
        fields = ('personalnummer', 'geschlecht', 'vorname', 'nachname', 'adresse', 'plz', 'ort', 'geburtsdatum', 'email', 'telefon', 'mobil', 'familienstand', 'kinder', 'besoldung', 'besoldungsstufe', 'innenauftragsnummer')

        widgets = {
            'personalnummer': forms.TextInput(attrs={'class': 'form-control'}),
            'geschlecht': forms.Select(attrs={'class': 'form-control'}),
            'vorname': forms.TextInput(attrs={'class': 'form-control'}),
            'nachname': forms.TextInput(attrs={'class': 'form-control'}),
            'adresse': forms.TextInput(attrs={'class': 'form-control'}),
            'plz': forms.TextInput(attrs={'class': 'form-control'}),
            'ort': forms.TextInput(attrs={'class': 'form-control'}),
            'geburtsdatum': forms.DateInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefon': forms.TextInput(attrs={'class': 'form-control'}),
            'mobil': forms.TextInput(attrs={'class': 'form-control'}),
            'familienstand': forms.Select(attrs={'class': 'form-control'}),
            'kinder': forms.NumberInput(attrs={'class': 'form-control'}),
            'besoldung': forms.TextInput(attrs={'class': 'form-control'}),
            'besoldungsstufe': forms.TextInput(attrs={'class': 'form-control'}),
            'innenauftragsnummer': forms.TextInput(attrs={'class': 'form-control'}),
        }

class EinsatzForm(forms.ModelForm):
    class Meta:
        model = Einsatz
        fields = ('startdatum', 'enddatum', 'einsatzbezeichnung', 'verantwortlicher', 'einsatzort', 'umfang')

        widgets = {
            'startdatum': forms.DateInput(attrs={'class': 'form-control'}),
            'enddatum': forms.DateInput(attrs={'class': 'form-control'}),
            'einsatzbezeichnung': forms.TextInput(attrs={'class': 'form-control'}),
            'verantwortlicher': forms.TextInput(attrs={'class': 'form-control'}),
            'einsatzort': forms.Select(attrs={'class': 'form-control'}),
            'umfang': forms.TextInput(attrs={'class': 'form-control'}),

        }

class EinsatzortForm(forms.ModelForm):
    class Meta:
        model = Einsatzort
        fields = ('standort_id', 'traegername', 'adresse', 'plz', 'ort', 'telefon', 'email', 'fax', 'traegerform')

        widgets = {
            'standort_id': forms.TextInput(attrs={'class': 'form-control'}),
            'traegername': forms.TextInput(attrs={'class': 'form-control'}),
            'adresse': forms.TextInput(attrs={'class': 'form-control'}),
            'plz': forms.NumberInput(attrs={'class': 'form-control'}),
            'ort': forms.TextInput(attrs={'class': 'form-control'}),
            'telefon': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'fax': forms.TextInput(attrs={'class': 'form-control'}),
            'traegerform': forms.Select(attrs={'class': 'form-control'}),
        }