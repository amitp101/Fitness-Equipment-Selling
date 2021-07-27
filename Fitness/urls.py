from django.contrib import admin
from django.urls import path, include
from admin1 import views
from user import views as view
from django.conf import settings
from django.conf.urls.static import static
#from user import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin1/', include('admin1.urls')),
    path('user/', include('user.urls')),
    path('visitor/', include('visitor.urls')),
    #path('', views.login)
    path('', view.index),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
 