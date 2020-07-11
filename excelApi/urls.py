from django.urls import path
from . import views

app_name = 'excelApi'

urlpatterns = [
    
    path('result/', views.excel_parse, name='parse'),
    path('upload/', views.link_upload, name='upload'),

]
