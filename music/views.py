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
def Userlogout(request):
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


# request for index page
@login_required(login_url='music:login')
def index(request):
    albums = Album.objects.all()

    return render(request,'music/index.html',{'albums':albums}) 



# request for detail page
@login_required(login_url='music:login')
def detail(request,pk):
    album = Album.objects.filter(id=pk)

    return render(request,'music/detail.html',{'album':album[0]})




# For Album Create
@login_required(login_url='music:login')
def AlbumCreate(request):
    form = AlbumForm(request.POST or None ,request.FILES or None)

    if form.is_valid():
        for prevalbum in Album.objects.all():
            album = form.save(commit=False)
            if prevalbum.album_title == album.album_title:
               return HttpResponse("There is already a album exisitng with this album title") 

        album = form.save()
        return redirect('music:detail',pk=album.id)

    return render(request,'music/album_form.html',{'form':form})




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

        form.save()
        return redirect('music:detail',pk=album.id)

    return render(request, "music/album_form.html",{'form':form})




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


