"""
URL configuration for day16 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path, re_path
from django.views.static import serve
from django.conf import settings

from app01.views import admin, account, task, upload, depart, user, prettynum, order, chart, city


urlpatterns = [
    # path('admin/', admin.site.urls),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}, name='media'),

    # 部门管理
    path('depart/list/', depart.depart_list),
    path('depart/add/', depart.depart_add),
    path('depart/delete/<int:nid>/', depart.depart_delete),
    path('depart/edit/<int:nid>/', depart.depart_edit),
    path('depart/multi/', depart.depart_multi),

    # 用户管理
    path('user/list/', user.user_list),
    path('user/add/', user.user_add),
    path('user/model/form/add/', user.user_model_form_add),
    path('user/edit/<int:nid>/', user.user_edit),
    path('user/delete/<int:nid>/', user.user_delete),

    # 靓号管理
    path('prettynum/list/', prettynum.prettynum_list),
    path('prettynum/create/', prettynum.prettynum_create),
    path('prettynum/edit/<int:nid>/', prettynum.prettynum_edit),
    path('prettynum/delete/<int:nid>/', prettynum.prettynum_delete),


    # 管理员管理
    path('admin/list/', admin.admin_list),
    path('admin/add/', admin.admin_add),
    path('admin/edit/<int:nid>/', admin.admin_edit),
    path('admin/delete/<int:nid>/', admin.admin_delete),
    path('admin/reset/<int:nid>/', admin.admin_reset),


    # 登录
    path('login/', account.login),
    path('image/code/', account.image_code),
    path('logout/', account.logout),
    # path('image/code/', account.image_code),

    # 任务管理
    path('task/list/', task.task_list),
    path('task/ajax/', task.task_ajax),
    path('task/add/', task.task_add),


    # 订单管理
    path('order/list/', order.order_list),
    path('order/add/', order.order_add),
    path('order/delete/', order.order_delete),
    path('order/detail/', order.order_detail),
    path('order/edit/', order.order_edit),

    path('chart/list/', chart.chart_list),
    path('chart/bar/', chart.chart_bar),
    path('chart/pie/', chart.chart_pie),
    path('chart/line/', chart.chart_line),


    path('upload/list/', upload.upload_list),
    path('upload/form/', upload.upload_form),
    path('upload/modalform/', upload.upload_modal_form),


    path('city/list/', city.city_list),
    path('city/add/', city.city_add),
]
