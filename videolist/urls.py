from django.urls import path

from videolist import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),  # 主页页面
    path('search/', views.Search.as_view(), name='search'),  # 搜索页面
    path('detail/<int:video_id>/', views.Detail.as_view(), name="video_detail"),  # 视频播放详情页面
    path('favorite/', views.Favorite.as_view(), name="favorite"),  # 喜欢
    path('collect/', views.Collect.as_view(), name="collect"),  # 收藏
    path('input_comment/<int:video_id>/', views.InputComment.as_view(), name="input_comment"),  # 输入评论
    path('upload/', views.Upload.as_view(), name="upload"),  # 投稿页面

]
