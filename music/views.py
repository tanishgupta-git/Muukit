from django.views import generic
from django.shortcuts import render, redirect , get_object_or_404
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login,logout

from .models import Album,Song
from .forms import CreateUserForm, AlbumForm, SongForm
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages

# import for restricting user to view some page
from django.contrib.auth.decorators import login_required
# Create your views here.

# File type defined for users
AUDIO_FILE_TYPES = ['wav', 'mp3', 'ogg']
IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']


# For Login Form Page
def UserLogin(request):
    if request.user.is_authenticated:
        return redirect('music:music')
    else:       
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user  = authenticate(request,username=username,password=password)

            if user is not None:
                login(request,user)
                return redirect('music:music')
            else:
                messages.info(request,'Username or Password is incorrect')

        context = {} 
        return render(request,'music/login.html',context)


#  Logout function
def UserLogout(request):
    logout(request)
    return redirect('music:login')



# For User Authentication
def UserRegister(request):
    if request.user.is_authenticated:
        return redirect('music:music')
    else:
        form = CreateUserForm()
        if request.method == "POST":
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request,"Account was created successfully " + user )
                return redirect('music:login')

        context = {'form':form}
        return render(request,'music/registration.html',context)


#Function for searching the user query 
def searchQuery(query,album):
    # for checking album info
    if query.lower() in album.album_title.lower() or query.lower() in album.artist.lower() or query.lower() in album.genre.lower():
        return True
    # for checking song info
    for song in album.song_set.all():
        if query in song.song_title:
            return True
    # if not matches
    return False


# request for index page
@login_required(login_url='music:login')
def index(request):
    albums = Album.objects.filter(user=request.user)
    return render(request,'music/index.html',{'albums':albums,'searchAlbum':True,'homeactive':True})


# Search page 
@login_required(login_url='music:login')
def search(request):
    search = request.GET.get('search')
    albums = Album.objects.filter(user=request.user)
    searchalbums = []
    for album in albums:
        if searchQuery(search,album):
            searchalbums.append(album)

    if not(len(searchalbums)):
        return render(request,'music/index.html',{'msg':True,'searchAlbum':True,'search':search,'homeactive':True})

    return render(request,'music/index.html',{'albums':albums,'searchAlbum':True,'homeactive':True}) 


# request for detail page
@login_required(login_url='music:login')
def detail(request,pk):
        user = request.user
        album = get_object_or_404(Album, pk=pk)
        return render(request,'music/detail.html',{'album':album})




# For Album Create
@login_required(login_url='music:login')
def AlbumCreate(request):
    form = AlbumForm(request.POST or None ,request.FILES or None)

    if form.is_valid():
        album = form.save(commit=False)
        for prevalbum in Album.objects.all():
            if prevalbum.album_title == album.album_title:
               return HttpResponse("There is already a album exisitng with this album title")

        #Restricting user to upload only three types of file 
        file_type = album.album_logo.url.split('.')[-1]
        file_type = file_type.lower()
        if file_type not in IMAGE_FILE_TYPES:
            return HttpResponse("Image file must be PNG,JPG, or JPEG")
  
        album.user = request.user
        album = form.save()

        return redirect('music:detail',pk=album.id)

    return render(request,'music/album_form.html',{'form':form,'addalbumactive':True,'pageheading':'Add New Album'})




# For Album Update
@login_required(login_url='music:login')
def AlbumUpdate(request,pk):
    album = get_object_or_404(Album,id=pk)
    
    form = AlbumForm(request.POST or None ,instance = album)
     
    if form.is_valid():
        for prevalbum in Album.objects.all():
            album = form.save(commit=False)
            if prevalbum.album_title == album.album_title:
               return HttpResponse("There is already a album exisitng with this album title")

        #Restricting user to upload only three types of file 
        file_type = album.album_logo.url.split('.')[-1]
        file_type = file_type.lower()
        if file_type not in IMAGE_FILE_TYPES:
            return HttpResponse("Image file must be PNG,JPG, or JPEG") 

        form.save()
        return redirect('music:detail',pk=album.id)

    return render(request, "music/album_form.html",{'form':form,'pageheading':'Update Album','fill':True,'album':album})




# For Album Delete
@login_required(login_url='music:login')
def AlbumDelete(request,pk):
    album = get_object_or_404(Album,id=pk)

    if request.method == "POST":
        album.delete()
        return redirect('music:music')

    return render(request, "music/album_delete_form.html")




# adding the song in album
@login_required(login_url='music:login')
def AddSong(request,pk):
    album = get_object_or_404(Album,id=pk)

    form = SongForm(request.POST or None ,request.FILES or None)
    if request.method == "POST":
        if form.is_valid():
            form_record = form.save(commit=False)
            for prevsong in album.song_set.all():
                if prevsong.song_title == form_record.song_title:
                    return HttpResponse("There is already a song exisitng with this song title")

        file_type = song.audio_file.url.split('.')[-1]
        file_type = file_type.lower()
        if file_type not in AUDIO_FILE_TYPES:
            return HttpResponse("Audio file must be WAV, MP3 or OGG")

            form_record.album = album
            form.save()
            return redirect('music:detail',pk=album.id) 
    
    return render(request,'music/song_form.html',{'form':form,'album':album})



# deleting the song from album
@login_required(login_url='music:login')
def DeleteSong(request,pk,songTitle):
    album = get_object_or_404(Album,id=pk)
     
    for song in album.song_set.all():
        if song.song_title == songTitle:
            song.delete()

    return redirect("music:detail",pk=album.id)


# Add To Favorite Songs
@login_required(login_url='music:login')
def Favorite(request,pk,songTitle,page):
    album = get_object_or_404(Album,id=pk)

    for song in album.song_set.all():
        if song.song_title == songTitle:
            song.is_favorite = not(song.is_favorite)
            song.save()
    if (page == 'songs'):
       return redirect("music:songs",userpreference ='all')
    else:
        return redirect("music:detail",pk=album.id)


# Add To Favorite Album
@login_required(login_url='music:login')
def FavoriteAlbum(request,pk):
    album = get_object_or_404(Album,id=pk)

    album.is_favorite = not(album.is_favorite)
    album.save()

    return redirect("music:music")


# All the song in user album 
@login_required(login_url='music:login')
def Songs(request,userpreference):
     albums = Album.objects.filter(user=request.user)
     
     songList = []

     if(userpreference == 'favorite'):
         for album in albums:
            for song in album.song_set.all():
                if(song.is_favorite):
                    songList.append(song)
     else:
        for album in albums:
            for song in album.song_set.all():
                songList.append(song)

     return render(request,'music/songs.html',{'songList':songList,'musicactive':True})