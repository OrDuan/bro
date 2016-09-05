from core.views import get_messages, get_bros, get_dashboard
from django.conf.urls import url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/user/message/get/', get_messages, name='core.get_messages'),
    url(r'^api/user/bro/get/', get_bros, name='core.get_bros'),
    url(r'^api/dashboard/get/', get_dashboard, name='core.get_dashboard'),
]
