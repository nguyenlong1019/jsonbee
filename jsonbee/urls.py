"""
URL configuration for jsonbee project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include 
from django.conf import settings 
from django.conf.urls.static import static 


urlpatterns = [
    path(f'{settings.ADMIN_ROUTE}/' if settings.ADMIN_ROUTE else 'admin/', admin.site.urls),
    path('', include('core.urls')),
]


# handler400 = 'core.views.error_page.custom_400_view'
# handler401 = 'core.views.error_page.custom_401_view'
# handler403 = 'core.views.error_page.custom_403_view'
# haneler404 = 'core.views.error_page.custom_404_view'
# handler500 = 'core.views.error_page.custom_500_view'


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
