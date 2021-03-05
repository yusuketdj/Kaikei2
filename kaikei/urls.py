from django.urls import path
from . import views

app_name = 'kaikei'

urlpatterns = [
    path('', views.top, name='top'),
    path('login/', views.loginfunc, name='login'),
    path('logout/', views.logoutfunc, name='logout'),
    path('index/', views.IndexView.as_view(), name='index'),
    path('change/<int:num>', views.change_waiting, name='change_waiting'),
    path('create/', views.CustomerCreate.as_view(), name='customer_create'),
    path('accounting/<int:num>', views.accounting, name='accounting'),
    path('accounting/result/', views.accounting_result, name='accounting_result'),
    path('accounting/result/send/', views.accounting_send, name='accounting_send'),
]