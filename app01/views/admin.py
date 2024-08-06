from django.shortcuts import render, HttpResponse, redirect
from django.core.exceptions import ValidationError
from app01 import models
from app01.models import Admin
from app01.utils.pagination import Pagination
from django import forms
from app01.utils.bootstrap import Bootstrap
from app01.utils.bootstrap import BootstrapForm
from app01.utils.encrypt import md5


def admin_list(request):
    # 管理员列表
    # 检查用户是否已经登录，已登录，继续，未登录跳转用户界面
    info_dict = request.session['info']
    if not info_dict:
        return redirect('/login/')

    queryset = Admin.objects.all()
    page_object = Pagination(request, queryset, query_field="username")

    context = {
        'page_list': page_object.page_queryset,
        'page_query': page_object.query_value,
        'page_string': page_object.html(),
    }
    return render(request, 'admin_list.html', context)


class AdminModelForm(Bootstrap, forms.ModelForm):
    confirm_password = forms.CharField(
        label='确认密码',
        widget=forms.PasswordInput(render_value=True),
    )

    class Meta:
        model = models.Admin
        fields = ["username", "password"]
        widgets = {
            'password': forms.PasswordInput(render_value=True),
        }

    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        return md5(pwd)

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get('password')
        confirm = md5(self.cleaned_data['confirm_password'])
        if not pwd == confirm:
            raise ValidationError('密码和验证密码不一致')
        return confirm


class AdminEditModelForm(Bootstrap, forms.ModelForm):
    class Meta:
        model = models.Admin
        fields = ["username"]


def admin_add(request):
    # 添加管理员
    title = "新建管理员"
    if request.method == 'GET':
        form = AdminModelForm()
        return render(request, 'change.html', {'title': title, 'form': form})

    form = AdminModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/admin/list/')

    return render(request, 'change.html', {'title': title, 'form': form})


def admin_edit(request, nid):
    row_object = models.Admin.objects.filter(id=nid).first()
    if not row_object:
        return redirect('/admin/list/')

    title = '编辑管理员'
    if request.method == 'GET':
        form = AdminEditModelForm(instance=row_object)
        return render(request, 'change.html', {'form': form, 'title': title})

    form = AdminEditModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/admin/list/')
    return render(request, 'change.html', {'form': form, 'title': title})


def admin_delete(request, nid):
    models.Admin.objects.filter(id=nid).delete()
    return redirect('/admin/list/')


class AdminResetModelForm(Bootstrap, forms.ModelForm):
    confirm_password = forms.CharField(
        label='确认密码',
        widget=forms.PasswordInput(render_value=True),
    )

    class Meta:
        model = models.Admin
        fields = ["password", "confirm_password"]
        widgets = {
            'password': forms.PasswordInput(render_value=True),
        }

    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        md5_pwd = md5(pwd)
        exists = models.Admin.objects.filter(id=self.instance.pk, password=md5_pwd).exists()
        if exists:
            raise ValidationError("密码不能与以前的密码的相同")
        return md5_pwd

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get('password')
        confirm = md5(self.cleaned_data['confirm_password'])
        if not pwd == confirm:
            raise ValidationError('密码和验证密码不一致')
        return confirm


def admin_reset(request, nid):
    row_object = models.Admin.objects.filter(id=nid).first()
    if not row_object:
        return redirect('/admin/list/')
    title = '重置密码-{}'.format(row_object.username)
    if request.method == 'GET':
        form = AdminResetModelForm()
        return render(request, 'change.html', {'form': form, 'title': title})
    form = AdminResetModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/admin/list/')
    return render(request, 'change.html', {'form': form, 'title': title})

