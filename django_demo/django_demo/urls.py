"""django_demo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from account import views as account_view
from django.conf.urls import url,include
from django.contrib import admin
from offer import views as offer_view

admin.autodiscover()

account_urlpatterns = [
    url(r'^login$', account_view.user_login, name='account_login'),
    url(r'^logout$', account_view.user_logout, name='account_logout'),
    url(r'^switchrole/(?P<new_role>[a-z A-Z]+)$', account_view.switch_role, name='account_switch_role'),
    url(r'^profile$', account_view.user_profile, name='account_profile'),
    url(r'^update$', account_view.user_update, name='account_update'),
    url(r'^changePWD$', account_view.user_changePWD, name='account_changePWD')
]

offer_urlpatterns = [
    url(r'^$', offer_view.offer_index, name="offer_index"),
    url('^(?P<offer_id>\d+)$', offer_view.offer_details, name="offer_details"),
    url('^add$', offer_view.offer_add, name="offer_add"),
    url('^generate/(?P<offer_id>\d+)$', offer_view.offer_generate, name="offer_generate"),
    url('^sign/(?P<offer_id>\d+)$', offer_view.offer_sign, name="offer_sign"),
    url('^download/(?P<offer_id>\d+)$', offer_view.offer_download, name="offer_download")
]

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', account_view.redirect_to_index),
    url(r'^index', account_view.redirect_to_index),
    url(r'^account/', include(account_urlpatterns)),
    url(r'^offer/', include(offer_urlpatterns)),
]

