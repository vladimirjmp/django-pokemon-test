from django.urls import path
from . import views

urlpatterns = [
    path('pokemon/<str:name>', views.PokemonApiView.as_view())
]
