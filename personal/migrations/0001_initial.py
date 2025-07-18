# Generated by Django 5.2.4 on 2025-07-06 15:33

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Diakon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('personalnummer', models.CharField(max_length=20, unique=True)),
                ('geschlecht', models.CharField(choices=[('m', 'Männlich'), ('w', 'Weiblich'), ('d', 'Divers')], max_length=10)),
                ('traeger', models.CharField(choices=[('elkb', 'ELKB'), ('diak_traeger', 'Diakonischer Träger'), ('sonst_traeger', 'Sonstiger Träger')], default='elkb', max_length=20)),
                ('vorname', models.CharField(max_length=50)),
                ('nachname', models.CharField(max_length=50)),
                ('adresse', models.CharField(max_length=200, null=True)),
                ('plz', models.CharField(max_length=10, null=True)),
                ('ort', models.CharField(max_length=100, null=True)),
                ('telefon', models.CharField(blank=True, max_length=30, null=True)),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('geburtsdatum', models.DateField()),
                ('familienstand', models.CharField(choices=[('ledig', 'Ledig'), ('verheiratet', 'Verheiratet'), ('geschieden', 'Geschieden'), ('verwitwet', 'Verwitwet')], max_length=20)),
                ('kinder', models.PositiveIntegerField(default=0)),
                ('besoldung', models.CharField(max_length=50)),
                ('besoldungsstufe', models.CharField(max_length=10)),
                ('innenauftragsnummer', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Einsatzort',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('standort_id', models.CharField(max_length=20, unique=True)),
                ('einsatzbezeichnung', models.CharField(blank=True, max_length=100, null=True)),
                ('adresse', models.TextField()),
                ('verantwortlicher', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Beurteilung',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datum', models.DateField()),
                ('note', models.PositiveIntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10'), (11, '11'), (12, '12'), (13, '13'), (14, '14'), (15, '15')])),
                ('beurteilende_person', models.CharField(max_length=50)),
                ('diakon', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='beurteilungen', to='personal.diakon')),
            ],
        ),
        migrations.CreateModel(
            name='Dokument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datei', models.FileField(upload_to='diakon_dokumente/')),
                ('hochgeladen_am', models.DateTimeField(auto_now_add=True)),
                ('beschreibung', models.CharField(blank=True, max_length=255)),
                ('diakon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dokumente', to='personal.diakon')),
            ],
        ),
        migrations.CreateModel(
            name='Einsatz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('startdatum', models.DateField()),
                ('enddatum', models.DateField(blank=True, null=True)),
                ('diakon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='personal.diakon')),
                ('einsatzort', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='personal.einsatzort')),
            ],
        ),
        migrations.CreateModel(
            name='Mitarbeiter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
                ('email', models.CharField(max_length=30, unique=True)),
                ('telefon', models.CharField(max_length=30, null=True)),
                ('abteilung', models.CharField(max_length=100, null=True)),
                ('ist_aktiv', models.BooleanField(default=True)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mitarbeiter', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Kontakt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datum', models.DateField(auto_now_add=True)),
                ('kontaktart', models.CharField(choices=[('telefon', 'Telefon'), ('email', 'E-Mail'), ('persoenlich', 'Persönlich'), ('brief', 'Brief')], default='telefon', max_length=20)),
                ('bearbeitungsstand', models.CharField(choices=[('offen', 'Offen'), ('in_bearbeitung', 'In Bearbeitung'), ('erledigt', 'Erledigt')], default='offen', max_length=20)),
                ('kontaktgrund', models.CharField(choices=[('allgemein', 'Allgemein'), ('versetzung', 'Versetzung'), ('teildienst', 'Teildienst'), ('beurlaubung', 'Beurlaubung'), ('beförderung', 'Beförderung'), ('krankheit', 'Krankheit'), ('fortbildung', 'Fortbildung'), ('ruhestand', 'Ruhestand'), ('besoldung', 'Besoldung'), ('rechtliches', 'Rechtliches'), ('sonstiges', 'Sonstiges')], max_length=20)),
                ('kommentar', models.TextField()),
                ('pk_ua', models.BooleanField(default=False, verbose_name='PK UA')),
                ('pe', models.BooleanField(default=False, verbose_name='PE')),
                ('diakon', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='kontakte', to='personal.diakon')),
                ('erfasser', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='personal.mitarbeiter')),
            ],
        ),
    ]
