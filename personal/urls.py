from django.urls import path
from . import views



urlpatterns = [
    path('', views.start, name='start'),
    path('personal/', views.personal, name='personal'),
    path('personal/<int:pk>/', views.person_detail, name='person_detail'),
    path('testseite/', views.testseite, name='testseite'),
    path('personal/<int:pk>/neuer_kontakt/', views.neuer_kontakt, name='neuer_kontakt'),
    path('personal/<int:pk>/edit_kontakt/<int:kontakt_pk>/', views.neuer_kontakt, name='edit_kontakt'),
    path('pkua/', views.pkua, name='pkua'),
    path('pe/', views.pe, name='pe'),
    path('search_personal/', views.search_personal, name='search_personal'),
    path('personal/neu/', views.neue_person, name='neue_person'),
    path('personal/<int:pk>/edit_person/', views.neue_person, name='edit_person'),
    path('personal/<int:pk>/neuer_einsatz/', views.neuer_einsatz, name='neuer_einsatz'),
    path('personal/<int:pk>/edit_einsatz/<int:einsatz_pk>/', views.neuer_einsatz, name='edit_einsatz'),
    path('personal/<int:pk>/generate_pdf/', views.generate_pdf, name='generate_pdf'),

]
