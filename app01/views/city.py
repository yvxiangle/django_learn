from django.shortcuts import render, redirect, HttpResponse
from app01 import models
from app01.utils.bootstrap import BootstrapForm


class UpModelForm(BootstrapForm):
    bootstrap_exclude_fields = ['logo']

    class Meta:
        model = models.City
        fields = '__all__'


def city_list(request):
    queryset = models.City.objects.all()
    context = {'city_list': queryset}
    return render(request, 'city_list.html', context)


def city_add(request):
    title = 'ModelForm上传'
    if request.method == 'GET':
        form = UpModelForm()
        context = {'title': title, 'form': form}
        return render(request, 'upload_form.html', context)
    form = UpModelForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        form.save()
        return redirect('/city/list/')
    context = {'title': title, 'form': form}
    return render(request, 'upload_form.html', context)
