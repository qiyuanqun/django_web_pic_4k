from django.conf.urls import url
from app_pic import views
from django.views.static import serve
from django.conf import settings
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(r'media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    url(r'^logout$', views.LogoutView.as_view(), name='logout'),
    url(r'^login$', views.LoginView.as_view(), name='login'),
    url(r'^register$', views.RegisterView.as_view(), name='register'),
    url(r'^file_download$', login_required(views.FileDownloadView.as_view()), name='file_download'),
    url(r'^file_desc$', login_required(views.FileDescView.as_view()),name='file_desc'),
    url(r'^file_show$', login_required(views.FileShowView.as_view()), name='file_show'),
    url(r'^file_upload$', login_required(views.FileUploadView.as_view()), name='file_upload'),
    url(r'^pic_detail$', views.DetailView.as_view(), name='pic_detail'),
    url(r'^$', views.IndexView.as_view(), name='index'),
]
