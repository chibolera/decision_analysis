from rest_framework import routers
from .views import MainFunctional, AgentStateViewSet
from django.urls import path, include

urlpatterns = [
    path('rates/<int:page>/', MainFunctional.as_view({'get':'get_rate'})),
    path('state/', AgentStateViewSet.as_view({'post':'create'})),
    path('', MainFunctional.as_view({'get':'retrieve', 'post':'create'})),
]