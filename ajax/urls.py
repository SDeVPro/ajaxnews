from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static 
from django.conf import settings
from news import views 
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('news.urls')),
    path('user_index/',views.user_index,name='user_index'),
    path('login/',views.login_form,name='login_form'),# /login/ {% url 'login_form' %} 
    path('logout/',views.logout_func,name='logout'),
    path('signup/',views.signup_form,name='signup_form'),
    path('category/<int:id>/<slug:slug>',views.category_news,name='category_news'),
    path('news/<int:id>/<slug:slug>',views.news_detail,name='news_detail'),
    path('update/',views.user_update,name='user_update'),
    path('password/',views.user_password,name='user_password'),
    path('comment/',views.user_comments,name='user_comments'),
    path('news/addcomment/<int:id>',views.addcomment,name='addcomment'),
    path('deletecomment/<int:id>',views.user_deletecomment,name='user_deletcomment'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
