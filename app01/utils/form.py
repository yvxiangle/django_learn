from app01.utils.bootstrap import BootstrapForm
from app01 import models
from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError


class EmployeeForm(BootstrapForm):
    # name = forms.CharField(min_length=3, label='用户名', error_messages={'required': '不能为空'})

    class Meta:
        model = models.Employee
        fields = ["name", "password", "age", "account", "create_time", "gender", "depart"]
        # widgets = {
        #     "name": forms.TextInput(attrs={'class': 'form-control'}),
        # }


class PrettyNumForm(BootstrapForm):
    mobile = forms.CharField(
        label="号码",
        validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误'),],
    )

    class Meta:
        model = models.PrettyNum
        fields = ['mobile', 'price', 'level', 'status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {'class': 'form-control'}

    def clean_mobile(self):
        txt_mobile = self.cleaned_data['mobile']
        if_exist = models.PrettyNum.objects.exclude(id=self.instance.id).filter(mobile=txt_mobile).exists()
        if if_exist:
            raise ValidationError('手机号已经存在')
        if len(txt_mobile) != 11:
            raise ValidationError('格式错误')
        return txt_mobile
