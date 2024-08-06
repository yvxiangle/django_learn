"""
自定义的分页组件
1, 获取数据库中所有的数据储存再 queryset中
    queryset = models.PrettyNum.objects.all()
2, 实例化分页对象
    page_project = Pagination(request, queryset)
3, 生成数据
    context = {'prettynum_list': pagination.page_queryset, 生成的数据列
           'query_value': pagination.query_value,   原始搜寻数据
           'page_string': pagination.html(),    生成的页码格式 （首页，上一页，页码，下一页，尾页 （） 跳转）
           }

"""
from django.utils.safestring import mark_safe


class Pagination(object):
    # request：网络请求
    # queryset：满足筛选条件的数据库数据对象集合
    # page_param：网页get请求发送页码的变量名称
    # query_value: 网页搜寻请求
    # query_field：搜索的字段名
    # page_size：每页显示数据量
    # plus：页码前后显示数量

    # display_page：显示多少页码
    def __init__(self, request, queryset,
                 page_param="page",
                 query_value="query_value",
                 query_field="",
                 page_size=20,
                 plus=3):

        import copy
        query_dict = copy.deepcopy(request.GET)
        query_dict._mutable = True
        self.query_dict = query_dict
        self.page_param = page_param

        # 初始化页码 page 页码字符
        page = request.GET.get(page_param, '1')
        if page.isdecimal():
            self.page = int(page)
        else:
            self.page = 1
        self.page_size = page_size

        # 搜寻条件
        data_dict = {}
        query_value = request.GET.get(query_value, '')
        self.query_value = query_value
        if self.query_value:
            data_dict['{}__contains'.format(query_field)] = self.query_value
        self.queryset_filter = queryset.filter(**data_dict).order_by("id")

        # 数据所显示的页数
        total_count = self.queryset_filter.count()
        total_page_count, div = divmod(total_count, page_size)
        if div:
            total_page_count += 1
        self.total_page_count = total_page_count
        self.plus = plus

        # 搜寻页码

        # 需要显示的数据统计
        self.start = (self.page - 1) * page_size
        self.end = self.start + page_size
        self.page_queryset = self.queryset_filter[self.start:self.end]

    def html(self):
        # 需要显示的页码判断
        if self.total_page_count <= 2 * self.plus + 1:
            start_page = 1
            end_page = self.total_page_count
        else:
            if self.page <= self.plus:
                start_page = 1
                end_page = 2 * self.plus + 1
            elif (self.page + self.plus) >= self.total_page_count:
                start_page = self.total_page_count - 2 * self.plus
                end_page = self.total_page_count
            else:
                start_page = self.page - self.plus
                end_page = self.page + self.plus

        page_str_list = []
        # 首页处理
        self.query_dict.setlist(self.page_param, [1])
        first_page = '<li><a href="?{}">首页</a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(first_page)
        # 上一页处理
        if self.page > 1:
            self.query_dict.setlist(self.page_param, [self.page - 1])
            prev = '<li><a href="?{}">上一页</a></li>'.format(self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_param, [self.page])
            prev = '<li><a href="?{}">上一页</a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(prev)

        # 中间页面的处理
        for i in range(start_page, end_page + 1):
            self.query_dict.setlist(self.page_param, [i])
            if i == self.page:
                ele = '<li class="active"><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            else:
                ele = '<li><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            page_str_list.append(ele)

        # 下一页处理
        if self.page < self.total_page_count:
            self.query_dict.setlist(self.page_param, [self.page + 1])
            down = '<li><a href="?{}">下一页</a></li>'.format(self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_param, [self.page])
            down = '<li><a href="?{}">下一页</a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(down)

        # 尾页处理
        self.query_dict.setlist(self.page_param, [self.total_page_count])
        last_page = '<li><a href="?{}">尾页</a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(last_page)

        search_string = """
          <li>
            <form style="float: left; margin-left: -1px" method="get" action="">
              <input type="text" style="position: relative; float: left;
                     display: inline-block; width: 90px;" name="query_page"
                     class="form-control" placeholder=' 页码 / {}'>
              <button class="btn btn-default" type="submit" style="color: #337ab7">跳转</button>
            </form>
          </li>
        """.format(self.total_page_count)
        page_str_list.append(search_string)
        page_string = mark_safe("".join(page_str_list))
        return page_string
