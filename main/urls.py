from django.urls.conf import path
from main import views 


app_name= 'main' # app_name은 해당 앱에 별칭을 부여함. (별칭 사용은 코드를 줄이기위함)

urlpatterns=[

    path('',views.get,name='get'),

    # url뒤에 index가 붙으면 views의 index함수를 호출하라는 뜻. name='index'는 별칭을 부여함.
]
