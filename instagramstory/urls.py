from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('views',
                       url(r'^$', 'index'),
                       url(r'^chooseImages/$', 'chooseImages'),
                       url(r'^viewResults/$', 'viewResults'),
                       )
