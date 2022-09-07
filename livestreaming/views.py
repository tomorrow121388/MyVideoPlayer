from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views import View

from livestreaming.models import LiveStreaming


class LiveStreamingView(View):
    def get(self, request):
        live_objs = LiveStreaming.objects.all()

        return render(request, "streamingindex.html", locals())


class LiveDetail(View):
    def get(self, request, live_id):
        live_detail_obj = LiveStreaming.objects.filter(id=live_id).first()

        return render(request, "livedetail.html", locals())


# def open_live(request):
#     send_video = SendVideo()
#     asyncio.run(send_video.main_logic(3))
#     return HttpResponse("0")

