from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views import generic
from django.views.decorators.cache import never_cache

# Views to recieve and return HTTP requests and responses back to the client
def home(request):
        return render(request, 'home.html')

def login_view(request):
        # Ensures the request method is POST and not GET
        if request.method=='POST':
            # Stores the username and password from the POST request in variables
            username = request.POST['username']
            password = request.POST['password']
            # Use Django's built-in authentication function for user credentials.
            # Will return user object if authenticated, "None" if not authenticated
            user = authenticate(request, username=username, password=password)
            # Login and Redirect to home if authenticated
            # If failed, give error message on login page           
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                error_message =  "Invalid username or password"
                return render(request, 'login.html', {'error_message': error_message})
        else:
            return render(request, 'login.html')

#Class based generic view used for form submissions(account creation)        
class signup_view(generic.CreateView):
     # Specifies to use UserCreationForm class for user creation
     form_class = UserCreationForm
     # Generic class-based views require reverse lazy as URLs not loaded
     success_url = reverse_lazy('login')
     # Refers to what template will displate the form
     template_name = 'signup.html'


def logout_view(request):
     logout(request)
     return redirect('home')

