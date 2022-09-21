from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns = [
    path('', views.index),
    path('earth-images', views.earth_image,name="earth-images"),
    path('mars',views.mars,name="mars"),
]

urlpatterns += staticfiles_urlpatterns()
