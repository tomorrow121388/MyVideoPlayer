from django import forms

from videolist.models import Video


class CommentForm(forms.Form):
    content = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    # content = forms.CharField(error_messages={'required': '不能为空', },
    #                           widget=forms.Textarea(attrs={'placeholder': '请输入评论内容'})
    #                           )


class UploadForm(forms.ModelForm):
    desc = forms.CharField(label="描述", max_length=70,
                           widget=forms.Textarea(
                               attrs={'class': 'form-control', "placeholder": "请输入内容...", "style": "resize:none"}))

    class Meta:
        model = Video
        fields = ["title", "video_group", "desc"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            if name == "desc":
                continue
            field.widget.attrs = {"class": "form-control", "placeholder": "请输入内容..."}
