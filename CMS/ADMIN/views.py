from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User
from APP.models import Attendance

# Create your views here.

def admin_login(request):
    try:
        if request.user.is_superuser:
            return redirect('/sup-admin/dashboard')

        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('pass')
            print(username, password)

            user_obj = authenticate(username=username, password=password)

            if not user_obj:
                messages.error(request, "Invalid username or password")
            elif not user_obj.is_superuser:
                messages.error(request, "You are not authorized to access this section")
            else:
                login(request, user_obj)
                return redirect('/sup-admin/dashboard')

    except Exception as e:
        print(f"Error: {e}")
        messages.error(request, "An unexpected error occurred. Please try again later.")

    content = {
        'title': 'Admin Login',
    }

    return render(request, 'admin_template/login.html', content)

def admin_dashboard(request):
    if request.user.is_superuser:
        if request.method == "POST":
            username = request.POST.get('username')
            data = Attendance.objects.filter(name=username)
            content = {
            'employee_records':data,
            'name':username
            }
            return render(request,'admin_template/admin_dashboard.html',content)
        return render(request,'admin_template/admin_dashboard.html')
    else:
        return redirect('/sup-admin/')
    
def logoutUser(request):
    logout(request)
    return redirect('/sup-admin/')

def search_employee(request):
    if request.method == "POST":
        username = request.POST.get('username')
        data = Attendance.objects.filter(name=username)
        content = {
            'employee_records':data
        }
    return redirect('/sup-admin/dashboard')