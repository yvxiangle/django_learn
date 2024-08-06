from django.shortcuts import render, HttpResponse
from django import forms
from app01.utils.bootstrap import Bootstrap, BootstrapForm
from app01 import models
import os
from django.conf import settings


def upload_list(request):
    if request.method == 'GET':
        return render(request, 'upload_list.html')
    file_obj = request.FILES.get('avatar')
    print(file_obj.name)

    path = r'E:\ProgramCode\pythonForWebLearn\day16\app01\media\{}'.format(file_obj.name)
    with open(path, 'wb+') as destination:
        for chunk in file_obj.chunks():
            destination.write(chunk)
    return HttpResponse('提交成功')


class UpForm(Bootstrap):
    bootstrap_exclude_fields = ['img']
    name = forms.CharField(label='姓名')
    age = forms.IntegerField(label='年龄')
    img = forms.FileField(label='头像')


def upload_form(request):
    title = 'Form上传'
    if request.method == 'GET':
        form = UpForm()
        context = {'title': title, 'form': form}
        return render(request, 'upload_form.html', context)
    form = UpForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        image_obj = form.cleaned_data.get('img')
        media_path = os.path.join(settings.MEDIA_ROOT, 'img', image_obj.name)
        db_media_path = os.path.join('media', 'img', image_obj.name)
        with open(media_path, 'wb') as destination:
            for chunk in image_obj.chunks():
                destination.write(chunk)
        models.Boss.objects.create(
            name=form.cleaned_data.get('name'),
            age=form.cleaned_data.get('age'),
            img=db_media_path,
        )
        return HttpResponse('上传成功')
    context = {'title': title, 'form': form}
    return render(request, 'upload_form.html', context)


class UpModelForm(BootstrapForm):
    bootstrap_exclude_fields = ['logo']

    class Meta:
        model = models.City
        fields = '__all__'


def upload_modal_form(request):
    title = 'ModelForm上传'
    if request.method == 'GET':
        form = UpModelForm()
        context = {'title': title, 'form': form}
        return render(request, 'upload_form.html', context)
    form = UpModelForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        form.save()
        return HttpResponse('上传成功')
    context = {'title': title, 'form': form}
    return render(request, 'upload_form.html', context)
