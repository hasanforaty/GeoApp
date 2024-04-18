from django.urls import path, include
from api.views import ShapeFileUploadApiView, FeaturesApiView, FeatureDetailApiView

urlpatterns = [
    path('shpefile/', ShapeFileUploadApiView.as_view()),
    path('layer/<layer_name>/features/', FeaturesApiView.as_view()),
    path('layer/<layer_name>/features/<pk>/', FeatureDetailApiView.as_view())

]
