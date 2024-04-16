from django.urls import path, include
from api.views import ShapeFileUploadApiView

urlpatterns = [
    path('shpefile/', ShapeFileUploadApiView.as_view())
]
