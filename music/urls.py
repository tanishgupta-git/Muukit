from django.urls import path
from . import views
app_name = 'music'
urlpatterns = [
    path('',views.Start, name='start'),
    path('index/', views.index, name='music'),
    path('register/', views.UserRegister, name='register'),
    path('login/',views.UserLogin,name='login'),
    path('logout/',views.UserLogout,name='logout'),
    path('<int:pk>/', views.detail, name="detail"),
    path('songs/<userpreference>/',views.Songs,name='songs'),
    path('album/add', views.AlbumCreate, name='album-add'),
    path('album/<int:pk>/', views.AlbumUpdate, name='album-update'),
    path('album/<int:pk>/delete/', views.AlbumDelete, name='album-delete'),
    path('album/<int:pk>/addsong/', views.AddSong, name='add-song'),
    path('album/<int:pk>/delete/<songTitle>/', views.DeleteSong, name='delete-song'),
    path('album/<int:pk>/<songTitle>/favorite/<page>/', views.Favorite, name='favorite'),
    path('album/<int:pk>/favorite/',views.FavoriteAlbum,name='favorite-album'),
    path('search/',views.Search,name='search'),
    path('song/search/',views.SearchSongs,name='search-songs')
] 