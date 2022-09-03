import json
import os
import time

import cv2
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, HttpResponse, redirect
from django.urls import reverse
from django.views import View
# from django.views.generic import ListView

from CustomTool.page_group import Pagination
from users.models import Users
from videolist.forms import CommentForm, UploadForm
from videolist.models import Video, Classification, Comment


class IndexView(View):
    def get(self, request):
        group_objs = Classification.objects.all()  # 分类的queryset对象
        slideshow_objs = Video.objects.order_by("-users_view_count")[0:3]

        g_id = request.GET.get("g_id", None)  # 分类id
        if g_id:
            video_group_obj = Video.objects.filter(video_group=g_id)
        else:
            video_group_obj = Video.objects.all()

        current_page = request.GET.get("page", 1)  # 分页
        all_count = video_group_obj.count()
        page_obj = Pagination(current_page=current_page, all_count=all_count, per_page_num=20)
        page_queryset = video_group_obj[page_obj.start:page_obj.end]

        return render(request, 'index.html', locals())


class Search(View):
    def get(self, request):
        search_words = request.GET.get("keywords")
        search_result_obj = Video.objects.filter(title__icontains=search_words)
        result_count = search_result_obj.count()

        current_page = request.GET.get("page", 1)
        page_obj = Pagination(current_page=current_page, all_count=result_count, per_page_num=20)
        page_queryset = search_result_obj[page_obj.start:page_obj.end]

        return render(request, 'search.html', locals())


class Detail(View):
    def get(self, request, video_id):
        current_user_obj = Users.objects.filter(id=request.session.get("user_id")).first()

        view_obj = Video.objects.filter(id=video_id).first()

        view_obj.users_view_count += 1
        view_obj.save()

        video_comment_count = view_obj.user_comment_count()

        user_obj = Users.objects.filter(id=view_obj.users_info.pk).first()
        favorite_static = view_obj.user_favorite_static(current_user_obj)
        collect_static = view_obj.user_collect_static(current_user_obj)

        comment_objs = Comment.objects.filter(video_comment=video_id).order_by("-create_time").all()  # 评论对象

        video_group_obj = view_obj.video_group  # 分组对象
        video_recommend_objs = Video.objects.filter(video_group=video_group_obj).order_by(
            "-users_view_count").all()[0:20]  # 视频推荐

        return render(request, 'video_detail.html', locals())


class Favorite(View):
    def get(self, request):
        video_id = request.GET.get("video_id")
        user_id = request.session.get("user_id")
        user_obj = Users.objects.filter(id=user_id).first()

        video_obj = Video.objects.filter(id=video_id).first()

        video_obj.user_favorite_rule(user_obj)

        video_favorite_counts = video_obj.user_favorite_count()
        video_favorite_static = video_obj.user_favorite_static(user_obj)

        print("video_favorite_counts", video_favorite_counts)

        data = {"video_favorite_counts": video_favorite_counts, "video_favorite_static": video_favorite_static}

        return JsonResponse(data)


class Collect(View):
    def get(self, request):
        video_id = request.GET.get("video_id")
        user_id = request.session.get("user_id")
        user_obj = Users.objects.filter(id=user_id).first()

        video_obj = Video.objects.filter(id=video_id).first()

        video_obj.user_collect_rule(user_obj)

        video_collect_counts = video_obj.user_collect_count()
        video_collect_static = video_obj.user_collect_static(user_obj)

        # print("video_favorite_counts", video_collect_counts)

        data = {"video_collect_counts": video_collect_counts, "video_collect_static": video_collect_static}

        return JsonResponse(data)


class InputComment(View):
    def post(self, request, video_id):
        content = request.POST.get("content")
        video_comment_obj = Video.objects.filter(id=video_id).first()
        user_id = request.session.get("user_id")
        user_comment_obj = Users.objects.filter(id=user_id).first()

        # if comment_form.is_valid():
        #     comment = comment_form.cleaned_data["content"]
        comment_obj = Comment.objects.create(video_comment=video_comment_obj, user_comment=user_comment_obj,
                                             content=content)
        comment_obj.save()

        return redirect(reverse('video_detail', args=(video_id,)))


class Upload(View):
    def get(self, request):
        video_form = UploadForm()
        return render(request, "upload.html", locals())

    def post(self, request):
        current_user_obj = Users.objects.filter(id=request.session.get("user_id")).first()

        # def post(self, request):
        video_form = UploadForm(request.POST)
        video_file = request.FILES['file']

        upload_video_url = os.path.join("videolist", "static", "video")  # 视频存储文件夹
        upload_cover_photo_url = os.path.join("videolist", "static", "cover_photo")  # 封面图片存储文件夹

        video_folder = os.path.exists(upload_video_url)
        cover_photo_folder = os.path.exists(upload_cover_photo_url)  # 封面图片存储文件夹
        if not video_folder:  # 如果没有文件夹就创建
            os.makedirs(upload_video_url)
        if not cover_photo_folder:
            os.makedirs(upload_cover_photo_url)

        if video_file:
            current_time = time.strftime("%Y%m%d%H%M%S")
            change_name = current_time + video_file.name
            save_video_url = f"static/video/{change_name}"
            finally_video_url = os.path.join(upload_video_url, change_name)
            video_name = video_file.name.split(".")  # 获取视频名字
            current_url = os.getcwd()  # 当前绝对路径
            current_video_url = os.path.join(current_url, finally_video_url)
            print(video_name)
            cover_photo_name = current_time + video_name[0] + ".jpg"  # 将视频名称拼接得到封面图名字

            finally_cover_photo_url = os.path.join(upload_cover_photo_url, cover_photo_name)  # 封面图片url
            print(cover_photo_name, "++++", finally_cover_photo_url)
            save_cover_photo_url = f"static/cover_photo/{cover_photo_name}"

            with open(finally_video_url, 'wb+') as f:
                for chunk in video_file.chunks():
                    f.write(chunk)

            self.save_video_cover_photo(current_video_url, finally_cover_photo_url)

        if video_form.is_valid():
            title = video_form.cleaned_data["title"]
            desc = video_form.cleaned_data["desc"]
            video_group = video_form.cleaned_data["video_group"]
            print("and12123", type(video_group), video_group.id)

            Video.objects.create(title=title, desc=desc, video_group_id=video_group.id, users_info=current_user_obj,
                                 file=save_video_url, cover_photo=save_cover_photo_url)
        return redirect(f"/space/{request.session.get('user_id')}")

    def save_video_cover_photo(self, video_url, cover_photo_url):
        videoCapture = cv2.VideoCapture(video_url)
        if videoCapture.isOpened():
            success, frame = videoCapture.read()
            if success:
                cv2.imwrite(cover_photo_url, frame)
