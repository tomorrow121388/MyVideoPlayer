from django.urls import path

from livestreaming import views

urlpatterns = [
    path('livestreaming/', views.LiveStreamingView.as_view(), name="livestreaming"),  # 直播主页页面
    path('livedetail/<int:live_id>/', views.LiveDetail.as_view(), name="livedetail"),  # 直播详情页
    # path('openlive/', views.open_live, name="openlive")
]
