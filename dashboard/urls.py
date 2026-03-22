from django.urls import path
from . import views
urlpatterns=[
    path('update/<int:id>/',views.update_report,name="update"),
    path('delete/<int:id>/',views.delete_report,name="delete"),
    path('', views.dashboard, name='dashboard'),
    path('reports/', views.reports, name='reports'),
    path('add/', views.add_report, name='add_report'),
    path('sign_up/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
     path('statistics/', views.statistics, name='statistics'),
   

]