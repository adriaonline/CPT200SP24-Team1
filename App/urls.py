from django.urls import path
from App import views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [ 
    # Calls home functions from views.py
    path("", views.home, name = "home"),
    # Assigns name and url access to login view
    path('login/', views.login_view, name='login'),
    # Assigns name and url access to signup view
    path('signup/', views.signup_view.as_view(), name='signup'),
    # Uses djangos Logout view and assigns name
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('upload/', views.upload_image, name='upload'),
    #Using the dynamic path parameters allows values to be passed from view
    path('result/<str:valid_tags>/<str:animal_names>/', views.result_view, name='result')
    
]
# Allows use of static files
urlpatterns+= static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)