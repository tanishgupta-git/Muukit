from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import render, redirect , get_object_or_404
from django.contrib.auth import authenticate, login
from django.views.generic import View
from .models import Album,Song
from .forms import UserForm , AlbumForm, SongForm
from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
# request for index page
def index(request):
    albums = Album.objects.all()

    return render(request,'music/index.html',{'albums':albums}) 

# request for detail page
def detail(request,pk):
    album = Album.objects.filter(id=pk)

    return render(request,'music/detail.html',{'album':album[0]})


# For Album Create
def AlbumCreate(request):
    form = AlbumForm(request.POST or None ,request.FILES or None)

    if form.is_valid():
        album = form.save()
        return redirect('music:detail',pk=album.id)

    return render(request,'music/album_form.html',{'form':form})


# For Album Update
def AlbumUpdate(request,pk):
    album = get_object_or_404(Album,id=pk)

    form = AlbumForm(request.POST or None ,instance = album)
     
    if form.is_valid():
        form.save()
        return redirect('music:detail',pk=album.id)

    return render(request, "music/album_form.html",{'form':form})



# For Album Delete
def AlbumDelete(request,pk):
    album = get_object_or_404(Album,id=pk)

    if request.method == "POST":
        album.delete()
        return redirect('music:music')

    return render(request, "music/album_delete_form.html")



# adding the song in album
def AddSong(request,pk):
    album = get_object_or_404(Album,id=pk)

    form = SongForm(request.POST or None ,request.FILES or None)
    if request.method == "POST":
        if form.is_valid:
            form_record = form.save(commit=False)
            form_record.album = album
            form.save()
            return redirect('music:detail',pk=album.id) 
    
    return render(request,'music/song_form.html',{'form':form,'album':album})






# For User Authentication
class UserFormView(View):
    form_class = UserForm
    template_name = 'music/registration_form.html'

    # display blank area
    def get(self,request):
        form = self.form_class(None)
        return render(request,self.template_name,{'form':form})
    # process form data
    def post(self,request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            # cleaned (normalized data)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            # return User objects if credentials are correct
            user = authenticate(username=username,password=password)
            
            if user is not None:

                if user.is_active:

                    login(request,user)
                    return redirect('music:music')

        return render(request, self.template_name, {'form':form})










