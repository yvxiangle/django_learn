from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from app01 import models
from app01.utils.bootstrap import BootstrapForm
from django.views.decorators.csrf import csrf_exempt
import random
from datetime import datetime
from app01.utils.pagination import Pagination


class OrderModelForm(BootstrapForm):
    class Meta:
        model = models.Order
        exclude = ['oid', 'admin']


def order_list(request):
    form = OrderModelForm()
    queryset = models.Order.objects.all().order_by('-id')
    pagination = Pagination(request, queryset, query_field="title")
    context = {
        'form': form,
        'queryset': queryset,
        'prettynum_list': pagination.page_queryset,
        'query_value': pagination.query_value,
        'page_string': pagination.html(),
    }
    return render(request, 'order_list.html', context)


@csrf_exempt
def order_add(request):
    form = OrderModelForm(data=request.POST)
    if form.is_valid():
        form.instance.oid = datetime.now().strftime('%Y%m%d%H%M%S') + str(random.randint(1000, 9999))
        form.instance.admin_id = request.session['info']['id']
        form.save()
        return JsonResponse({'status': True})
    return JsonResponse({'status': False, 'errors': form.errors})


def order_delete(request):
    uid = request.GET.get('uid')
    exists = models.Order.objects.filter(id=uid).exists()
    if not exists:
        return JsonResponse({'status': False, 'error': '数据异常，数据不存在'})
    models.Order.objects.filter(id=uid).delete()
    return JsonResponse({'status': True})


def order_detail(request):
    # uid = request.GET.get('uid')
    # exists = models.Order.objects.filter(id=uid).exists()
    # if not exists:
    #     return JsonResponse({'status': False, 'error': '数据异常，数据不存在'})
    # row_object = models.Order.objects.filter(id=uid).first()
    # res = {
    #     'status': True,
    #     'result': {
    #         'title': row_object.title,
    #         'price': row_object.price,
    #         'status': row_object.status,
    #     }
    # }
    # return JsonResponse(res)
    uid = request.GET.get('uid')
    exists = models.Order.objects.filter(id=uid).exists()
    if not exists:
        return JsonResponse({'status': False, 'error': '数据异常，数据不存在'})
    row_object = models.Order.objects.filter(id=uid).values('title', 'price', 'status').first()
    res = {
        'status': True,
        'data': row_object,
    }
    return JsonResponse(res)


@csrf_exempt
def order_edit(request):
    uid = request.GET.get('uid')
    row_object = models.Order.objects.filter(id=uid).first()
    if not row_object:
        return JsonResponse({'status': False, 'tips': '数据异常，数据不存在'})
    form = OrderModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return JsonResponse({'status': True})
    return JsonResponse({'status': False, 'errors': form.errors})
