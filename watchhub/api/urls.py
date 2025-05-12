from django.urls import path
from rest_framework.routers import DefaultRouter
from watchhub.api.views import (StreamPlatformVS,
                                WatchContentListAV,
                                WatchContentIndividualAV,
                                ContentReviewListGv,
                                ContentReviewIndividualGv,
                                ContentReviewCreateGv)

router=DefaultRouter()
router.register(r'streamplatform',StreamPlatformVS)
urlpatterns=router.urls
urlpatterns+=[
    path('watch-content/',WatchContentListAV.as_view(),name='watch-content-list'),
    path('watch-content/<int:pk>/',WatchContentIndividualAV.as_view(),name='watch-content-individual'),

    path('content/<int:pk>/review/',ContentReviewListGv.as_view(),name='review-content-list'),
    path('content/<int:pk>/review-create/',ContentReviewCreateGv.as_view(),name='review-content-create'),
    path('contentreview/<int:pk>/',ContentReviewIndividualGv.as_view(),name='watch-content-individual')
]

# path('api/stream/',StreamPlatformListAV.as_view(),name='stream'),
# path('api/stream/<int:pk>/',StreamPlatformIndividualAV.as_view(),name='streamplatform-detail'),
# path('api/contentreview/',ContentReviewListGv.as_view(),name='review-content-list'),
