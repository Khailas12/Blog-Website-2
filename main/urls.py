from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic.base import TemplateView
from mysite.views import create_blog, blog_view
from django.contrib.auth.views import LogoutView
from user_auth import views as auth_view
# from user_auth.views import signup
from django.conf.urls import url



urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html')),
    path('blog/', create_blog),
    path('blog/<int:pk>/', blog_view),
    
    # url(r'^signup/$', auth_view.signup, name='signup'),
    path('signup/', auth_view.signup, name='signup'),
    path('sent/', auth_view.activation_sent_view, name='activation_sent'),
    path('activate/<slug:uidb64>/<slug:token>', auth_view.activate, name='activate'),

    path('admin/', admin.site.urls),
]

#  path() always matches the complete path, so path('account/login/') is equivalent to url('^account/login/$') .