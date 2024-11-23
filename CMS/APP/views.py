from django.shortcuts import render,HttpResponse,redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import logout,login as auth_login ,authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from APP.models import Attendance
from datetime import datetime

# Create your views here.

@login_required(login_url='/')
def home(request):
    user_id = request.user.id
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return HttpResponse("User does not exist", status=404)
    
    dataa = Attendance.objects.filter(userid=user_id)

    current_date = datetime.now().date()
    blocked = 'none'
    
    for data in dataa:
        if str(current_date) == str(data.datetime):  # Assuming `data.datetime` is a DateTimeField
            blocked = 'disabled'
            break  # Stop the loop if a match is found

    content = {
        'title':'Home',
        'name':user.username,
        'maintext':'Hello this is home page',
        'block':blocked
    }
    return render(request,'index.html',content)

def login(request):
    if request.user.is_authenticated:
        return redirect('/home')
    
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('pass')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # If the user with the given email does not exist, show an error message
            messages.error(request, 'Invalid email or password.')
            return render(request, 'login.html')
        
        # Authenticate with username if using default Django settings
        # You need to adjust this if you use email for authentication
        user = authenticate(username=user.username, password=password)

        if user is not None:
            auth_login(request, user)  # Use the `login` function from `django.contrib.auth`
            return redirect('/home')
        else:
            messages.error(request, 'Invalid email or password.')
            return render(request, 'login.html')
    content = {
        'title':'Login',
        'maintext':'Hello this is home page'
    }
    return render(request,'login.html',content)

def singup(request):
    if request.user.is_authenticated:
        return redirect('/home')
    content = {
        'title':'Singup'
    }
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('pass')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken.')
            return render(request, 'singup.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already registered.')
            return render(request, 'singup.html')
        
        # Create the user if no duplicates are found
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        print(email,password)
        return redirect('/')
    return render(request,'singup.html',content)

def logoutUser(request):
    logout(request)
    return redirect('/')

def present(request):
    if request.method == "POST":
        user_id = request.user.id
        user = get_object_or_404(User, id=user_id)
        current_date = datetime.now().date()
        value = request.POST.get('action')
        Attendance.objects.create(userid=user_id,name=user.username,status=value,datetime=current_date)
        return redirect('/home')
    return redirect('/home')