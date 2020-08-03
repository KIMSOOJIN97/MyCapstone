
from django.contrib import admin
from django.urls import path
from django.urls.conf import include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('',include('main.urls')), # url주소 뒤에 아무것도 기입하지 않으면 main의 urls.py 로 가라는 뜻
]