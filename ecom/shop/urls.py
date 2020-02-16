from django.urls import path
from .import views

urlpatterns = [
    path("",views.index,name='index'),
    path("about/",views.about,name='about'),
    path("contact/",views.contact,name='contact'),
    path("tracker/",views.tracker,name='tracker'),
    path("product/<product_id>",views.product,name='product'),
    path("search/",views.search,name='search'),
    path("checkout/",views.checkout,name='checkout'),
    path("login/",views.getlogin,name='login'),
    path("logout/",views.getlogout,name='logout'),
    path("register/",views.register,name='register'),
    path("userprofile/",views.userprofile,name='userprofile')

] 