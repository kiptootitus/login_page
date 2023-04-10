from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from pymongo import MongoClient


def home(request):
    context = {
        'welcome_message': 'Welcome to my website!'
    }
    return render(request, 'home.html', context)

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        # Check if passwords match
        if password != confirm_password:
            return render(request, 'register/register.html', {'error': 'Passwords do not match'})
        
        # Check if username or email already exists
        if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
            return render(request, 'register/register.html', {'error': 'Username or email already exists'})
        
        # Save user to MongoDB database
        client = MongoClient('mongodb+srv://eco:Titus1@3@cluster0.je0rm.mongodb.net/?retryWrites=true&w=majority')
        db = client['toshcode']
        users = db['users']
        user_data = {'username': username, 'email': email, 'password': password}
        result = users.insert_one(user_data)
        print('User added with ID:', result.inserted_id)
        
        # Redirect to login page
        return redirect('login')
    
    return render(request, 'register/register.html')
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Connect to your MongoDB instance using PyMongo
        client = MongoClient('mongodb://localhost:27017/')
        db = client['your_database_name']
        users_collection = db['your_users_collection_name']

        # Look up the user by username and password hash in your MongoDB database
        user_data = users_collection.find_one({'username': username, 'password_hash': hash(password)})
        
        if user_data:
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('home') # Replace 'home' with the name of your desired home view

    return render(request, 'login/login.html')

#login_required
def account(request):
    user = request.user
    context = {
        'user': user,
    }
    return render(request, 'account/account.html', context)

def user_logout(request):
    logout=request.user
    context = {
        'logout': logout,
    }    
    return redirect(request,'home', context)