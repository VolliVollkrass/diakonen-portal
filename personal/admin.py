from django.contrib import admin
from .models import Mitarbeiter, Diakon, Kontakt, Dokument, Beurteilung, Einsatzort, Einsatz, Pkua

# Register your models here.
admin.site.register(Mitarbeiter)
admin.site.register(Diakon)
admin.site.register(Kontakt)
admin.site.register(Dokument)
admin.site.register(Beurteilung)
admin.site.register(Einsatzort)
admin.site.register(Einsatz)
admin.site.register(Pkua)
