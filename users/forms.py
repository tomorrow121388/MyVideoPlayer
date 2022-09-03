from django import forms

from users.models import Users


class UserForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=11, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="密码", max_length=16, widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class RegisterForm(forms.Form):
    gender_choices = (
        (1, "男"),
        (0, "女"),
    )
    username = forms.CharField(label="账号", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="确认密码", max_length=256,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    mobile = forms.CharField(label="手机号", widget=forms.TextInput(attrs={'class': 'form-control'}))
    gender = forms.ChoiceField(label='性别', choices=gender_choices)
    nickname = forms.CharField(label="用户名", max_length=11, widget=forms.TextInput(attrs={'class': 'form-control'}))


class SettingFrom(forms.ModelForm):

    # avatar = forms.ImageField(label="头像")

    class Meta:
        model = Users
        fields = ["nickname", "gender", "introduct"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": "请输入内容..."}
