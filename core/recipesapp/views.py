from django.shortcuts import render,redirect
from .models import Recipes
from django.contrib import messages
from django.contrib.auth import login, logout,authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Create your views here.

@login_required(login_url="/login_page/")
def home(request):
    queryset = Recipes.objects.all()

    if request.GET.get('search'):
        queryset = queryset.filter(recipe_name__icontains = request.GET.get('search'))

    return render(request, 'index.html', context={'page':"home", "recipes_list": queryset})

def recipe(request):
    if request.method == "POST":
        data = request.POST
        recipe_name = data.get('recipe_name')
        recipe_description = data.get('recipe_description')
        recipe_image = request.FILES.get('recipe_image')

        Recipes.objects.create(
        recipe_name = recipe_name,
        recipe_description = recipe_description,
        recipe_image = recipe_image
        )
        return redirect('/home/')    
    
    
    return render(request, 'Recipes.html')

def update_recipe(request, id):
    queryset = Recipes.objects.get(id = id)

    if request.method == 'POST':
        data = request.POST
        recipe_name = data.get('recipe_name')
        recipe_description = data.get('recipe_description')
        recipe_image = request.FILES.get('recipe_image')

        queryset.recipe_name = recipe_name
        queryset.recipe_description = recipe_description

        if recipe_image:
            queryset.recipe_image = recipe_image

        queryset.save()
        return redirect("/home/")
    
    context = {"recipes": queryset}
    return render(request, 'update_recipes.html', context)



def delete_recipe(request,id):
    queryset = Recipes.objects.get(id=id)
    queryset.delete()
    return redirect('/home/')
    

def login_page(request):

    if request.method == "POST":
        data = request.POST
        username = data.get("username")
        password = data.get("password")

        if not User.objects.filter(username = username).exists():
            messages.info(request,"Invalid Username")
            return redirect('/login_page/')
        
        user = authenticate(username=username, password= password)

        if user is None:
            messages.info(request,"Invalid Password")
            return redirect('/login_page/')
        else:
            login(request,user)
            return redirect('/home/')

    return render(request, 'login.html')

def logout_page(request):
    logout(request)
    return redirect('/login_page/')
    

def register(request):

    if request.method == "POST":
        data = request.POST
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        username = data.get('username')
        password = data.get('password')
        

        user = User.objects.filter(username=username)

        if user.exists():
            messages.info(request,"Username already exists")
            print("Username already exists")
            return redirect('/register/')

        user = User.objects.create(
            first_name = first_name,
            last_name = last_name,
            username = username
        )
        user.set_password(password)
        user.save()

        return redirect("/login_page/")
    return render(request, 'register.html')
    

