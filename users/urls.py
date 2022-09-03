from django.urls import path

from users import views

urlpatterns = [
    path('login/', views.Login.as_view(), name="login"),  # 登录页面
    path('register/', views.Register.as_view(), name="register"),  # 注册页面
    path('logout/', views.Logout.as_view(), name="logout"),  # 注销页面
    path('space/<int:user_id>/', views.Space.as_view(), name="space"),  # 个人中心页面
    path('space_liked/<int:user_id>/', views.UserLiked.as_view(), name="user_liked"),  # 个人中心喜欢页面
    path('space_collect/<int:user_id>/', views.UserCollect.as_view(), name="user_collect"),  # 个人中心收藏页面
    path('setting/<int:user_id>/', views.UserSetting.as_view(), name="user_setting"),  # 个人中心修改资料页面

]
