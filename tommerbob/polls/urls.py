from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

app_name = "polls"

urlpatterns = [
    path('', views.index, name='index'),
    path('home', views.index, name='index'),
    path('account', views.account, name='account'),
    path('<int:beverage_id>/', views.beverage_details, name='detail'),
    path('<int:beverage_id>/new_order/', views.new_order, name="new_order"),
    path('login', views.login_request, name="login"),
    path('logout', views.logout_view, name="logout"),
]

urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)