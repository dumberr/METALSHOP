from django.urls import path, re_path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("info/", views.info, name="info"),
    path("log/", views.log, name="log"),
    
    path("istoric/", views.istoric, name="istoric"),
    path("despre/", views.despre, name="despre"),
    
    # ^ inceputul adresei, ?P<id> valoarea parametrului id, [0-9]+ unul sau mai multe cifre, $ 
    re_path(r"^accesare(?P<id>[0-9]+)/$", views.detalii_accesare, name="detalii_accesare"),
    
    
    path("produse/", views.in_lucru, name="produse"),
    path("contact/", views.in_lucru, name="contact"),
    path("cos_virtual/", views.in_lucru, name="cos_virtual"),
]