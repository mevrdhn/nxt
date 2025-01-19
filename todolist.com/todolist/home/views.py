from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import ToDoList, Item
from .forms import CreateNewList

# Create your views here.

def index(response, names):
    ls = ToDoList.objects.filter(name__startswith=names)
    for lss in ls:
        if response.method == "POST":
            if response.POST.get("save"):
                for item in lss.item_set.all():
                    if response.POST.get("c"+str(item.id)) == "clicked":
                        item.complete = True
                    else:
                        item.complete = False
                    item.save()
                
            
            elif response.POST.get("newItem"):
                txt = response.POST.get("new")

                if len(txt) > 2:
                    lss.item_set.create(text=txt, complete=False)
            
            elif response.POST.get("delete"):
                txt = response.POST.get("new")

                dele = lss.item_set.get(text=txt)
                dele.delete()
    return render(response, "home/list.html", {"ls":ls, "names":names})

def home(response):
    nmlist = ToDoList.objects.prefetch_related('item_set').all()
    if response.method == "POST":
        t = response.POST.get("input")
        if response.POST.get("save"):
            if len(t) != 0 :
                ToDoList(name=t).save()
            for todolist in nmlist:
                for item in todolist.item_set.all():
                    if response.POST.get("s"+str(item.id)) == "clicked":
                        item.complete = True
                    else:
                        item.complete = False
                    item.save()

        if response.POST.get("deleted"):
            if len(t) != 0:
                t1 = ToDoList.objects
                dele = t1.filter(name__startswith=t)
                for ite in dele:
                    ite.delete()
            
    return render(response, "home/home.html", {"nmlist":nmlist})

def create(response):
    if response.method == "POST":
        form = CreateNewList(response.POST)
        if form.is_valid():
            if response.POST.get("save"):
                n = form.cleaned_data["name"]
                t = ToDoList(name=n)
                t.save()
            if response.POST.get("delete"):
                t1 = ToDoList.objects
                dele = t1.filter(name__startswith=n)
                for item in dele:
                    item.delete()

    else:    
        form = CreateNewList()
    return render(response, "home/create.html", {"form":form})