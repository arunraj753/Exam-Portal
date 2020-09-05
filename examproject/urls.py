from django.contrib import admin
from django.urls import path,include
from accounts import views as user_views 
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from examonline import views as exviews
urlpatterns = [
    path('',include('examonline.urls')),
    path('admin/', admin.site.urls),
    path('index',user_views.index,name='index'),
    path('register/teacher',user_views.teacher_registration,name='register-teacher'),
    path('register/student',user_views.student_registration,name='register-student'),
    path('login',auth_views.LoginView.as_view(template_name='accounts/login.html'),name='login'),
    path('logout',auth_views.LogoutView.as_view(template_name='accounts/logout.html'),name='logout'),
    path('password/update',user_views.change_password,name='password-change'),
    path('account',user_views.account,name='account'),
 
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
#if settings.DEBUG:
 #       urlpatterns += static(settings.MEDIA_URL,
  #                            document_root=settings.MEDIA_ROOT)