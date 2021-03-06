from django.shortcuts import render, redirect
from django.http import HttpResponse
from lists.models import Item, List
from django.core.exceptions import ValidationError
from lists.forms import ExistingListItemForm, ItemForm
from django.views.generic import FormView, CreateView, DetailView

from django.contrib.auth import get_user_model
User = get_user_model()

# Create your views here

def home_page(request):
     return render(request,'home.html', {'form':ItemForm()})

def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    form = ExistingListItemForm(for_list=list_)
    if request.method == 'POST':
        form = ExistingListItemForm(for_list=list_, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(list_)
    return render(request, 'list.html', {'list': list_, "form": form})

def new_list(request):
    form = ItemForm(data=request.POST)
    if form.is_valid():
        list_ = List()
        if request.user.is_authenticated:
            list_.owner = request.user
        list_.save()
        form.save(for_list=list_)
        return redirect(list_)
    else:
        return render(request, 'home.html', {"form": form})

class HomePageView(FormView):
    template_name = 'home.html'
    form_class = ItemForm

class NewListView(CreateView):
    form_class = ItemForm
    template_name = 'home.html'

    def form_valid(self, form):
        list_ = List.objects.create()
        form.save(for_list=list_)
        return redirect(list_)

class ViewAndAddToList(DetailView,CreateView):
    model = List
    template_name='list.html'
    form_class = ExistingListItemForm

    def get_form(self):
        self.object = self.get_object()
        return self.form_class(for_list=self.object,data=self.request.POST)

def my_lists(request, email):
    owner = User.objects.get(email=email)
    return render(request, 'my_lists.html', {'owner': owner})

def share_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    list_.shared_with.add(request.POST['sharee'])
    return redirect(list_)


