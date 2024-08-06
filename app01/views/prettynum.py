from django.shortcuts import redirect, render
from app01 import models
from app01.utils.pagination import Pagination
from app01.utils.form import PrettyNumForm


def prettynum_list(request):
    queryset = models.PrettyNum.objects.all()
    pagination = Pagination(request, queryset, query_field="mobile")

    context = {
        'prettynum_list': pagination.page_queryset,
        'query_value': pagination.query_value,
        'page_string': pagination.html(),
    }
    return render(request, 'prettynumList.html', context)


def prettynum_create(request):
    if request.method == 'GET':
        form = PrettyNumForm()
        return render(request, 'prettynumCreate.html', {'form': form})
    form = PrettyNumForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('/prettynum/list')
    return render(request, 'prettynumCreate.html', {'form': form})


def prettynum_edit(request, nid):
    # row_obj = models.PrettyNum.objects.filter(id=nid).first()
    # print(row_obj)
    row_obj = models.PrettyNum.objects.get(id=nid)
    print(row_obj)
    if request.method == 'GET':
        form = PrettyNumForm(instance=row_obj)
        return render(request, 'prettynumEdit.html', {'form': form})
    form = PrettyNumForm(request.POST, instance=row_obj)
    if form.is_valid():
        form.save()
        return redirect('/prettynum/list/')
    return render(request, 'prettynumEdit.html', {'form': form})


def prettynum_delete(request, nid):
    row_obj = models.PrettyNum.objects.get(id=nid)
    row_obj.delete()
    return redirect('/prettynum/list/')

