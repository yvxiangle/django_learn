from django.shortcuts import render, redirect
from app01 import models
from app01.utils.pagination import Pagination
from app01.utils.form import EmployeeForm


def user_list(request):
    queryset = models.Employee.objects.all()
    page_object = Pagination(request, queryset)
    # 用户管理
    context = {
        'employees': page_object.page_queryset,
        'page_string': page_object.html()
    }
    return render(request, 'user_list.html', context)


def user_add(request):
    if request.method == "GET":
        context = {
            'gender_choices': models.Employee.gender_choice,
            'depart_list': models.Department.objects.all()
        }
        return render(request, 'user_add.html', context)

    # 获取用户提交的数据
    name = request.POST.get('employee_name')
    print(name)
    password = request.POST.get('employee_password')
    print(password)
    age = request.POST.get('employee_age')
    print(age)
    account = request.POST.get('employee_account')
    print(account)
    create_time = request.POST.get('employee_ctime')
    print(create_time)
    gender = request.POST.get('employee_gender')
    print(gender)
    department = request.POST.get('employee_department')
    print(department)

    models.Employee.objects.create(name=name, password=password, age=age,
                                   account=account, create_time=create_time,
                                   gender=gender, depart_id=department)

    return redirect('/user/list/')


def user_model_form_add(request):
    if request.method == "GET":
        form = EmployeeForm()
        return render(request, 'user_model_form_add.html', {'form': form})
    form = EmployeeForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/user/list/')
    # 校验失败（在页面上显示错误信息）
    return render(request, 'user_model_form_add.html', {'form': form})


def user_edit(request, nid):
    # 根据ID去数据库获取需要编辑的数据
    row_object = models.Employee.objects.filter(id=nid).first()
    if request.method == "GET":
        form = EmployeeForm(instance=row_object)
        return render(request, 'user_edit.html', {'form': form})

    form = EmployeeForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/user/list/')
    return render(request, 'user_edit.html', {'form': form})


def user_delete(request, nid):
    models.Employee.objects.filter(id=nid).delete()
    return redirect('/user/list/')

