from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from employee import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('employee_attendance.urls')),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
