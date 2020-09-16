from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import View
from .models import Album,Song
from .forms import UserForm , AlbumForm
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
class AlbumCreate(CreateView):
    model = Album
    fields = ['artist','album_title','genre','album_logo']



# For Adding Song
class AddSong(CreateView):
    model = Song
    fields = ['file_type','song_title','is_favorite']

# For Album Update
class AlbumUpdate(UpdateView):
    model = Album
    fields = ['artist','album_title','genre','album_logo']

# For Album Delete
class AlbumDelete(DeleteView):
    model = Album
    success_url = reverse_lazy('music:music')

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










