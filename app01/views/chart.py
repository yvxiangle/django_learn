from django.shortcuts import render
from django.http import HttpResponse, JsonResponse


def chart_list(request):
    return render(request, 'chart_list.html')


def chart_bar(request):
    # 构造柱状图的数据
    legend = ['销量', '业绩']
    series_list = [
        {
            'name': '销量',
            'type': 'bar',
            'data': [5, 20, 36, 10, 10, 20]
        },
        {
            'name': '业绩',
            'type': 'bar',
            'data': [45, 10, 66, 20, 20, 10]
        }
    ]
    x_axis = ['1月', '2月', '4月', '5月', '6月', '7月']
    result = {
        'status': True,
        'data': {
            'legend': legend,
            'series': series_list,
            'xAxis': x_axis,
        },
    }
    return JsonResponse(result)


def chart_pie(request):
    db_data_list = [
        {'value': 1048, 'name': 'IT部门'},
        {'value': 735, 'name': '运营'},
        {'value': 580, 'name': '新媒体'},
    ]

    result = {
        'status': True,
        'data': db_data_list
    }

    return JsonResponse(result)


def chart_line(request):
    x_axis_data = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    series_data = [150, 230, 224, 218, 135, 147, 260]
    res = {
        'status': True,
        'data': {
            'xAxis': x_axis_data,
            'series': series_data,
        },
    }
    return JsonResponse(res)
