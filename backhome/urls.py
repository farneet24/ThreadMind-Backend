from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'urls', views.URLModelViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/storeComments/', views.store_comments),
    path('stream/<str:session_id>/', views.Summary),
    path('stream/<str:session_id>/keywords/', views.Keywords),
    path('sentiment/', views.fetch_sentiment),
    path('emotion/', views.fetch_emotion),
    path('cyber/', views.fetch_cyber),
]
