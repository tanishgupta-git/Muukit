from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import View
from .models import Album
from .forms import UserForm
# Create your views here.
class IndexView(generic.ListView):
    template_name = 'music/index.html'
    # by default it will return the albums with object_list name but if you want to change than you can do like this

    def get_queryset(self):
        return Album.objects.all()

class DetailView(generic.DetailView):
    model = Album
    template_name = 'music/detail.html'


class AlbumCreate(CreateView):
    model = Album
    fields = ['artist','album_title','genre','album_logo']

class AlbumUpdate(UpdateView):
    model = Album
    fields = ['artist','album_title','genre','album_logo']

class AlbumDelete(DeleteView):
    model = Album
    success_url = reverse_lazy('music:music')

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










