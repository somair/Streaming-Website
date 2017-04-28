from django.views import  generic
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import  authenticate, login
from django.core.urlresolvers import reverse_lazy
from django.views.generic import View
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Album
from .forms import UserForm
from .serializers import AlbumSerializer

class IndexView(generic.ListView):
    template_name = 'music/index.html'
    context_object_name = 'all_albums'

    def get_queryset(self):
        return Album.objects.all()

class DetailView(generic.DetailView):
    model = Album
    template_name = 'music/detail.html'

class AlbumCreate(CreateView):
    model = Album
    fields = {'album_logo','genre','album_title','artist'}

class AlbumUpdate(UpdateView):
    model = Album
    fields = {'album_logo', 'genre', 'album_title', 'artist'}

class AlbumDelete(DeleteView):
    model = Album
    success_url = reverse_lazy('music:index')

class UserFormView(View):
    form_class = UserForm
    template_name = 'music/registration_form.html'

   #display blank form
    def get(self,request):
        form =self.form_class(None)
        return render(request,self.template_name,{'form':form})

    #process form data
    def post(self,request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            # cleaned (normalized) data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            #return User objects if credentials are correct

            user = authenticate(username=username, password=password)
            if user is not None : #유저가 존재할경우
                if user.is_active :
                    # 유저가 정지당하거나 로그인 불가능한 경우가 아닌 경우
                    login(request,user)
                    return redirect('music:index')


#List all albums or create a new album
#albumlists/1
class AlbumList(APIView):

    def get(self,request):
        albums = Album.objects.all()
        serializer = AlbumSerializer(albums, many=True)
        return Response(serializer.data)

    def post(self):
        pass