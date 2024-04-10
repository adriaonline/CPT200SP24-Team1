from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView
from django.views import generic
from django.views.decorators.cache import never_cache
from .forms import ImageUploadForm
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials
from .models import ImageUploadModel, DetectedObject, AnimalNames
from io import BytesIO



# Views to recieve and return HTTP requests and responses back to the client
def home(request):
        form = ImageUploadForm
        return render(request, 'home.html', {'form': form})

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

def upload_image(request):
     # Ensures form is a post method and had valid data input
     if request.method == 'POST':
          form = ImageUploadForm(request.POST, request.FILES)
          if form.is_valid():
               
               # Save the current form to a variable and get the path to that image file
               image_instance = form.save()
               image_path = image_instance.image.path

               #Normally store endpoint and key outside of program, but left in for group purposes
               endpoint = 'https://petnamer.cognitiveservices.azure.com/'
               key = '0f9e940c4f32467d95b1e34e91c0c954'

               #Create a vision client with the endpoint and key provided by Azure
               client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(key))
               
               #Use the current uploaded image, in binary mode, so it can be read to Azure
               with open(image_path, "rb") as image_file:
                    image_stream = BytesIO(image_file.read())
                    
                    #Analyze the current image using the Azure client and returning the tags for the image
                    result = client.analyze_image_in_stream(image_stream, visual_features=[VisualFeatureTypes.tags])
                    
               #Extract detected names from the analysis results
               detected_tags = [tag.name for tag in result.tags]

               #Filters for only tags of animals(ignore background)
               valid_tags = [tag for tag in detected_tags if tag.lower() in ('dog', 'cat', 'bird', 'cow', 'hamster', 'snake')]

               #Send tag to AnimalNames model to look for that species, and return names associated
               animal_names = AnimalNames.objects.filter(species__in=valid_tags).values_list('name', flat=True)
               for name in animal_names: print(name)
          
          #Redirect to the result page where it will display the speices and animal names
          return redirect('result', valid_tags=valid_tags, animal_names=list(animal_names))
     #If form isn't valid, reload form as empty 
     else: 
        form = ImageUploadForm()
        return render(request, 'home.html', {'form': form})
               
def result_view(request, valid_tags, animal_names):
     #Retrieves the image that was last uploaded and gets the url of said image
     last_image = ImageUploadModel.objects.last()
     image_url = last_image.image.url if last_image else None

     #Use stripping and splitting to format the appearance of the animal species and names
     valid_tags = valid_tags.strip('[]').split(', ')
     animal_names = animal_names.strip('[]').split(',')
     for name in animal_names:
          print(name)
     
     # collect a context variable of all data that will be passed to the Result.html
     context = {'image_url': image_url, 'animal_names': animal_names, 'valid_tags': valid_tags}
     return render(request, 'result.html', context)
