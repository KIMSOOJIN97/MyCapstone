from django.shortcuts import render
from django.http import HttpResponse
from urllib.request import urlopen
from urllib.parse import quote_plus

from .models import InsertDb5 # 모델에서 Resource를 불러온다


def get(request):
 
    insta = InsertDb5.objects.all()
    insta_list = {'insta_list' : insta}
    return render(request, 'main/home.html',insta_list)
 