from django.urls import path, include
from api.views import ShapeFileUploadApiView, FeatureApiView

urlpatterns = [
    path('shpefile/', ShapeFileUploadApiView.as_view()),
    path('layer/<layer_name>/features/',FeatureApiView.as_view())
]
