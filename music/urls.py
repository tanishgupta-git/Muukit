from django.urls import path
from . import views
app_name = 'music'
urlpatterns = [
    path('', views.index, name='music'),
    path('<int:album_id>/', views.detail, name="detail"),
#     for favorites song
    path('<int:album_id>/favorite', views.favorite, name="favorite")
]