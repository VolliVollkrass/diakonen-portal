from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import KontaktForm, DiakonForm, EinsatzForm, EinsatzortForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import FileResponse
#Django imports for PDF generation
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch


def start(request):
    return render(request, 'personal/start.html')

@login_required
def personal(request):
    diakone = Diakon.objects.all()
    letzter_einsatz = Einsatz.objects.order_by('-startdatum').first()
    alter = Diakon.alter  # Get the most recent Einsatz
    return render(request, 'personal/personal.html', {'diakone': diakone, 'letzter_einsatz': letzter_einsatz, 'alter': alter})

@login_required
def person_detail(request, pk):
    diakon = get_object_or_404(Diakon, pk=pk)

    #Zugriff auf verbundene Daten
    kontakte = diakon.kontakte.all()
    dokumente = diakon.dokumente.all()
    beurteilungen = diakon.beurteilungen.all()
    einsaetze = diakon.einsaetze.all()
    # Wenn der Diakon keine Einsätze hat, kann letzter_einsatz None sein
    letzter_einsatz = einsaetze.order_by('-startdatum').first() if einsaetze.exists() else None
    aktueller_einsatz = letzter_einsatz.einsatzort.standort_id if letzter_einsatz else None
    aktueller_einsatzort = letzter_einsatz.einsatzort if letzter_einsatz else None
    aktueller_einsatzadresse = aktueller_einsatzort.adresse if aktueller_einsatzort else "Nicht zugewiesen"
    aktueller_einsatzverantwortlicher = letzter_einsatz.verantwortlicher if letzter_einsatz else "Nicht zugewiesen"
    aktuelle_einsatzfunktion = letzter_einsatz.einsatzbezeichnung if letzter_einsatz else "Nicht zugewiesen"
    aktuelle_einsatztelefon = aktueller_einsatzort.telefon if aktueller_einsatzort else "Nicht zugewiesen"
    aktueller_einsatzemail = aktueller_einsatzort.email if aktueller_einsatzort else "Nicht zugewiesen"
    aktuelle_einsatzfax = aktueller_einsatzort.fax if aktueller_einsatzort else "Nicht zugewiesen"

    return render(request, 'personal/person_detail.html', {'diakon': diakon, 'kontakte': kontakte, 'dokumente': dokumente, 'beurteilungen': beurteilungen, 'einsaetze': einsaetze, 'aktueller_einsatz': aktueller_einsatz, 'aktueller_einsatzort': aktueller_einsatzort, 'aktueller_einsatzadresse': aktueller_einsatzadresse, 'aktueller_einsatzverantwortlicher': aktueller_einsatzverantwortlicher, 'aktuelle_einsatzfunktion': aktuelle_einsatzfunktion, 'aktuelle_einsatztelefon': aktuelle_einsatztelefon, 'aktueller_einsatzemail': aktueller_einsatzemail, 'aktuelle_einsatzfax': aktuelle_einsatzfax   })

def testseite(request):
    diakone = Diakon.objects.all()
    kontakte = Kontakt.objects.all()
    dokumente = Dokument.objects.all()
    beurteilungen = Beurteilung.objects.all()
    einsatzorte = Einsatzort.objects.all()
    einsatze = Einsatz.objects.all()
    letzter_einsatz = einsatze.order_by('-startdatum').first()  # Get the most recent Einsatz
    return render(request, 'personal/testseite.html', {'diakone': diakone, 'kontakte': kontakte, 'dokumente': dokumente, 'beurteilungen': beurteilungen, 'einsatzorte': einsatzorte, 'einsatze': einsatze, 'letzter_einsatz': letzter_einsatz})

@login_required
def neuer_kontakt(request, pk, kontakt_pk=None):
    kontakt = get_object_or_404(Kontakt, pk=kontakt_pk) if kontakt_pk else None
    if request.method == 'POST':
        form = KontaktForm(request.POST, instance=kontakt)
        if form.is_valid():
            kontakt = form.save(commit=False)
            kontakt.erfasser = request.user.mitarbeiter
            kontakt.diakon = get_object_or_404(Diakon, pk=pk)
            kontakt.save()
            return redirect('person_detail', pk=kontakt.diakon.pk)  # Redirect to the detail page of the diakon
    else:
        form = KontaktForm(instance=kontakt)
    return render(request, 'personal/neuer_kontakt.html', {'form': form})

@login_required
def neue_person(request, pk=None):
    diakon = get_object_or_404(Diakon, pk=pk) if pk else None
    if request.method == 'POST':
        form = DiakonForm(request.POST, instance=diakon)
        if form.is_valid():
            diakon = form.save(commit=False)
            diakon.erstellt_durch = request.user.mitarbeiter  # Set the creator of the diakon
            diakon.erstellt_am = timezone.now()  # Set the creation date
            diakon.save()
            return redirect('person_detail', pk=diakon.pk)  # Redirect to the detail page of the new diakon
    else:
        form = DiakonForm(instance=diakon)
    return render(request, 'personal/neue_person.html', {'form': form})

@login_required
def neuer_einsatz(request, pk, einsatz_pk=None):
    einsatz = get_object_or_404(Einsatz, pk=einsatz_pk) if einsatz_pk else None
    if request.method == 'POST':
        form = EinsatzForm(request.POST, instance=einsatz)
        if form.is_valid():
            einsatz = form.save(commit=False)
            einsatz.diakon = get_object_or_404(Diakon, pk=pk)
            einsatz.save()
            return redirect('person_detail', pk=einsatz.diakon.pk)
    else:
        form = EinsatzForm(instance=einsatz)
    return render(request, 'personal/neuer_einsatz.html', {'form': form})



@login_required
def pkua(request):
    diakon = Diakon.objects.all()  # Get all diakons
    pkua_kontakt = Kontakt.objects.filter(pk_ua=True).order_by('-datum')  # Filter for PK UA contacts
    pkua = Pkua.objects.all()

    return render(request, 'personal/pkua.html', {'diakon': diakon, 'pkua_kontakt': pkua_kontakt})

@login_required
def pe(request):
    diakon = Diakon.objects.all()  # Get all diakons
    pe = Kontakt.objects.filter(pe=True).order_by('-datum')  # Filter for PE contacts

    return render(request, 'personal/pe.html', {'diakon': diakon, 'pe': pe})

@login_required
def search_personal(request):
    if request.method == 'POST':
        searched = request.POST.get('searched', '')
        diakone = Diakon.objects.filter(nachname__contains=searched) | Diakon.objects.filter(vorname__contains=searched) | Diakon.objects.filter(personalnummer__contains=searched)  # Filter diakons by last name
        return render(request, 'personal/search_personal.html', {'searched': searched, 'diakone': diakone})
    else:
        return render(request, 'personal/search_personal.html', {})
#    query = request.GET.get('q', '')
#    diakone = Diakon.objects.filter(name__icontains=query)  # Filter diakons by name
#    return render(request, 'personal/search_personal.html', {'diakone': diakone, 'query': query})


# Generate a PDF report
@login_required
def generate_pdf(request, pk):
    buf = io.BytesIO()
    diakon = get_object_or_404(Diakon, pk=pk)
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    width, height = letter
    textob = c.beginText()
    textob.setFont("Helvetica", 12)
    textob.setTextOrigin(1 * inch, 1 * inch)

    #lines = [
    #    f"Name: {diakon.vorname} {diakon.nachname}",
    #    f"Personalnummer: {diakon.personalnummer}",
    #    f"Geburtsdatum: {diakon.geburtsdatum}",
    #    f"Alter: {diakon.alter()} Jahre",
    #    f"Telefon: {diakon.telefon}",
    #    f"E-Mail: {diakon.email}",
    #]
    lines = []
    kontakt = diakon.kontakte.all()
    lines.append(f"Personalnummer: {diakon.personalnummer}")
    lines.append(f"Name: {diakon.vorname} {diakon.nachname}")
    lines.append(f"Telefon: {diakon.telefon}")
    lines.append(f"E-Mail: {diakon.email}")
    lines.append(f"Geburtsdatum: {diakon.geburtsdatum}")
    lines.append(f"Alter: {diakon.alter()} Jahre")
    lines.append("Kontakte:")
    for k in kontakt:
        lines.append(f"Am {k.datum} über {k.kontaktart} mit dem Kontaktgrund {k.kontaktgrund} - {k.kommentar} unter dem Bearbeitungsstand {k.bearbeitungsstand}")
    
    
    for line in lines:
        textob.textLine(line)

    c.drawText(textob)
    c.showPage()
    c.save()

    buf.seek(0)
    return FileResponse(buf, as_attachment=True, filename=f"diakon_{diakon.personalnummer}.pdf")

@login_required
def einsatzorte (request):
    einsatzorte = Einsatzort.objects.all()

    return render(request, 'einsatz/einsatzorte.html',{'einsatzorte': einsatzorte} )

@login_required
def neuer_einsatzort (request, pk=None):
    einsatzort = get_object_or_404(Einsatzort, pk=pk)if pk else None
    if request.method == 'POST':
        form = EinsatzortForm(request.POST, instance=einsatzort)
        if form.is_valid():
            einsatzort = form.save(commit=True)
            return redirect('einsatzorte')
    else:
        form = EinsatzortForm(instance=einsatzort)
    return render(request, 'einsatz/neuer_einsatzort.html', {'form': form})