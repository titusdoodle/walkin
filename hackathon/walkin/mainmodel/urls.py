from django.conf.urls import url
from mainmodel import views

urlpatterns = [
    url(r'^home/', views.home, name="home"),
    url(r'^register/', views.register, name="register"),
    url(r'^login/', views.login_mod, name="login"),
    url(r'^logout/', views.logout_met, name="logout"),
    url(r'^recommender/', views.recommender, name="recommender"),
    url(r'^getstarted/', views.getstarted, name="getstarted"),
]