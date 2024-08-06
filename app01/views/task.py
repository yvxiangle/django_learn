from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from app01.utils.form import BootstrapForm
from app01 import models
from django import forms
from app01.utils.pagination import Pagination


class TaskModelForm(BootstrapForm):
    class Meta:
        model = models.Task
        fields = '__all__'
        widgets = {
            "detail": forms.TextInput(attrs={'class': 'form-control'}),
        }


def task_list(request):
    form = TaskModelForm()
    queryset = models.Task.objects.all().order_by('-id')

    page_object = Pagination(request, queryset, query_field="admin")

    context = {
        'form': form,
        'queryset': queryset,
        'page_query': page_object.query_value,
        'page_string': page_object.html(),
    }

    return render(request, 'task_list.html', context)


@csrf_exempt
def task_ajax(request):
    data_dict = {'status': True, 'data': [11, 22, 33, 44]}
    json_string = json.dumps(data_dict)
    return HttpResponse(json_string)


@csrf_exempt
def task_add(request):
    form = TaskModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        data_dict = {'status': True}
        json_string = json.dumps(data_dict)
        return HttpResponse(json_string)
    date_dict = {'status': False, 'error': form.errors}
    return HttpResponse(json.dumps(date_dict, ensure_ascii=False))
