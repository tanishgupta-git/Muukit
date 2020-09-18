from django.urls import path
from . import views
app_name = 'music'
urlpatterns = [
    path('', views.index, name='music'),
    path('register/', views.UserFormView.as_view(), name='register'),
    path('<int:pk>/', views.detail, name="detail"),
    path('album/add', views.AlbumCreate, name='album-add'),
    path('album/<int:pk>/', views.AlbumUpdate, name='album-update'),
    path('album/<int:pk>/delete', views.AlbumDelete, name='album-delete'),
    path('album/<int:pk>/addsong', views.AddSong, name='add-song'),
    path('album/<int:pk>/delete/<songTitle>', views.DeleteSong, name='delete-song')
] 