
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('', include('personal.urls')),
    path('data_wizard/', include('data_wizard.urls')),
    # Authentication URLs
    path('accounts/login/', views.LoginView.as_view(), name='login'),
    path('accounts/logout/', views.LogoutView.as_view(next_page='/'), name='logout'),
]
