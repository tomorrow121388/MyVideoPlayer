import datetime
import hashlib
import os
import time

from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views import View

from CustomTool.page_group import Pagination
from users.forms import UserForm, RegisterForm, SettingFrom
from users.models import Users
from videolist.models import Video


def hash_code(s, salt='like_akl'):
    """ 密码加密 """
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()


class Login(View):
    def post(self, request):
        if request.session.get('is_login'):
            return redirect('/')

        login_form = UserForm(request.POST)
        message = "所有字段不能为空！"
        if login_form.is_valid():  # 用户名字符合法验证 使用表单类自带的is_valid()方法一步完成数据验证工作；
            username = login_form.cleaned_data['username']  # 验证成功后可以从表单对象的cleaned_data数据字典中获取表单的具体值
            password = login_form.cleaned_data['password']
            try:
                user = Users.objects.get(username=username)
                if user.password == hash_code(password):
                    request.session['is_login'] = True
                    request.session['user_id'] = user.pk
                    request.session['user_name'] = user.username
                    request.session['nickname'] = user.nickname
                    # print("--------------", request.session.get('user_name'))
                    return redirect('/')
                else:
                    message = "账号或密码错误！"
            except:
                message = "用户名不存在！"
        login_form = UserForm()
        return render(request, 'login.html', locals())

    def get(self, request):
        if request.session.get('is_login'):
            return redirect('/')
        login_form = UserForm()
        return render(request, 'login.html', locals())


class Register(View):
    def post(self, request):
        if request.session.get('is_login'):  # 账号已经登录不允许注册
            return redirect('/')

        register_form = RegisterForm(request.POST)
        message = '请检查填写的内容'

        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            mobile = register_form.cleaned_data['mobile']
            gender = register_form.cleaned_data['gender']
            nickname = register_form.cleaned_data['nickname']

            if password1 != password2:
                message = '两次输入密码不同，请重新输入'
                return render(request, 'register.html', locals())
            else:
                user = Users.objects.filter(username=username)
                if user:
                    message = "账号已存在，请重新输入"
                    return render(request, 'register.html', locals())

            new_user = Users.objects.create(
                username=username, password=hash_code(password1), mobile=mobile, gender=gender, nickname=nickname
            )
            # new_user.username = username
            # new_user.password = hash_code(password1)
            # new_user.mobile = mobile
            # new_user.gender = gender
            new_user.save()

            return redirect('login')  # 自动跳转到登录页面

        register_form = RegisterForm()
        return render(request, 'register.html', locals())

    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', locals())


class Logout(View):
    def post(self, request):
        # request.session.flush()  # session中的所有内容全部清空
        # del request.session['is_login']
        # del request.session['user_id']
        # del request.session['user_name']
        return redirect('/')

    def get(self, request):
        request.session.flush()  # session中的所有内容全部清空
        return redirect('/')


class Space(View):
    def get(self, request, user_id):
        space_user_obj = Users.objects.filter(id=user_id).first()

        space_video_objs = space_user_obj.video_set.all()
        all_count = space_video_objs.count()
        current_page = request.GET.get("page", 1)
        page_obj = Pagination(current_page=current_page, all_count=all_count, per_page_num=20)
        page_queryset = space_video_objs[page_obj.start:page_obj.end]

        return render(request, "space.html", locals())


class UserLiked(View):
    def get(self, request, user_id):
        space_user_obj = Users.objects.filter(id=user_id).first()

        liked_video_objs = Video.objects.filter(users_favorite=space_user_obj.id).all()
        all_count = liked_video_objs.count()
        current_page = request.GET.get("page", 1)
        page_obj = Pagination(current_page=current_page, all_count=all_count, per_page_num=20)
        page_queryset = liked_video_objs[page_obj.start:page_obj.end]

        return render(request, "user_liked.html", locals())


class UserCollect(View):
    def get(self, request, user_id):
        space_user_obj = Users.objects.filter(id=user_id).first()

        collect_video_objs = Video.objects.filter(users_collection=space_user_obj).all()
        all_count = collect_video_objs.count()
        current_page = request.GET.get("page", 1)
        page_obj = Pagination(current_page=current_page, all_count=all_count, per_page_num=20)
        page_queryset = collect_video_objs[page_obj.start:page_obj.end]

        return render(request, "user_collect.html", locals())


class UserSetting(View):
    def get(self, request, user_id):
        space_user_obj = Users.objects.filter(id=user_id).first()

        initial_data = {"nickname": space_user_obj.nickname, "introduct": space_user_obj.introduct,
                        "gender": space_user_obj.gender}  # 设置输入框默认值
        setting_from = SettingFrom(initial=initial_data)

        return render(request, "user_setting.html", locals())

    def post(self, request, user_id):
        setting_from = SettingFrom(request.POST)

        img_obj = request.FILES.get("file")  # 获取文件对象

        upload_url = os.path.join("users", "static", "avatar", f"{user_id}")
        avatar_folder = os.path.exists(upload_url)
        if not avatar_folder:
            os.makedirs(upload_url)  # 如果没有文件夹就创建

        if img_obj:
            current_time = time.strftime("%Y%m%d%H%M%S")
            change_name = current_time + img_obj.name
            img_name = f"static/avatar/{user_id}/{change_name}"
            pic_url = os.path.join(upload_url, change_name)
            with open(pic_url, 'wb') as pic_file:
                for i in img_obj.chunks():
                    pic_file.write(i)
        else:
            user_obj = Users.objects.filter(id=user_id).first()
            img_name = user_obj.avatar

        if setting_from.is_valid():
            nickname = setting_from.cleaned_data['nickname']
            introduct = setting_from.cleaned_data['introduct']
            gender = setting_from.cleaned_data['gender']

            Users.objects.filter(id=user_id).update(nickname=nickname, introduct=introduct, gender=gender,
                                                    avatar=img_name)
            # update_user_info.save()
        return redirect(f"/setting/{user_id}/")
