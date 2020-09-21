from django.conf.urls import url

from .views import(

	view_ipk,

)

urlpatterns = [
	
	url(r'^view_id/(?P<pk>\d+)/$', view_ipk, name="view_ipk")

]