from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import View
from .models import Album,Song
from .forms import UserForm

# Create your views here.
class IndexView(generic.ListView):
    template_name = 'music/index.html'

    def get_queryset(self):
        return Album.objects.all()

# For Detail View Of Album
class DetailView(generic.DetailView):
    model = Album
    template_name = 'music/detail.html'

# For Album Create
class AlbumCreate(CreateView):
    model = Album
    fields = ['artist','album_title','genre','album_logo']



# For Adding Song
class AddSong(CreateView):
    model = Song
    fields =  ['file_type','song_title','is_favorite']
    def get(self,request):
        specifAlbum = request.GET.get(pk)
        
        


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










