import hashlib
import os
import re

from django.conf import settings
from django.shortcuts import render, redirect
from django.utils.encoding import escape_uri_path
from django.views.generic import View
from app_pic.models import Pic_4k, UploadFile, User
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse, FileResponse
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse

# Create your views here.

class IndexView(View):
    '''首页'''

    # /index?cls='4k美女'&page=2
    def get(self, request):
        # 获取cls参数
        cls = request.GET.get('cls','4k美女')
        all_cls_pic = Pic_4k.objects.filter(img_cls=cls)

        # 按每页20条数据进行分页
        paginator = Paginator(all_cls_pic,20)

        # 获取page参数
        try:
            page = int(request.GET.get('page', 1))
        except:
            page = 1

        # 设计页码范围
        page_range = None
        page_count = paginator.num_pages
        if page_count <= 7:
            page_range = range(1, page_count + 1)
        else:
            if page <= 4:
                page_range = range(1, 8)
            elif page >= page_count - 3:
                page_range = range(page_count - 6, page_count + 1)
            else:
                page_range = range(page - 3, page + 4)

        # 实例化page对象
        page_pic = paginator.page(page)
        content = {
            'cls': cls,
            'page_pic': page_pic,
            'page_range': page_range,
        }
        return render(request, 'index.html', content)

class DetailView(View):
    '''4k图片详情页'''

    # /index?pic_id=1
    def get(self,request):
        try:
            pic_id = int(request.GET.get('pic_id'))
            pic = Pic_4k.objects.get(id=pic_id)
        except Pic_4k.DoesNotExist:
            return HttpResponse('没有这张图片!!!')
        except Exception:
            return HttpResponse('传入的id是非数字!!!')
        content = {
            'pic': pic
        }
        return render(request, 'pic_detail.html', content)

class FileUploadView(View):
    '''文件上传'''
    def get(self, request):
        return render(request, 'file_upload.html')

    def post(self, request):
        file = request.FILES.get('file')
        file_desc = request.POST.get('file_desc')
        if not all([file, file_desc]):
            return JsonResponse({'msg': '数据不完整'})

        # 文件名以及文件大小
        file_name = file.name
        file_size = file.size

        # 创建md5对象
        m = hashlib.md5()
        for content in file.chunks():
            # 更新md5值
            m.update(content)
        file_md5 = m.hexdigest()

        # 判断文件夹中是否已经有该文件
        # 文件后缀名
        Suffix = re.findall(r'\.\w*', file_name)[-1]
        file_path = file_md5 + Suffix

        save_path = '%s%s' % (settings.MEDIA_ROOT, file_path)

        is_exist = os.path.isfile(save_path)
        print(is_exist)
        if not is_exist:
            with open(save_path, 'wb') as f:
                for content in file.chunks():
                    f.write(content)

        # 在数据库中保存记录
        user = request.user
        try:
            user_file = UploadFile.objects.get(file_name=file_name, file_path=file_path, file_user=user)  # 注意———关联传入的是对象
            return JsonResponse({'msg': '你已上传过该文件'})
        except UploadFile.DoesNotExist:
            UploadFile.objects.create(file_name = file_name,file_desc=file_desc,file_path = file_path,file_size = file_size,file_user = user)
            return JsonResponse({'msg': '上传成功'})

class FileShowView(View):
    def get(self, request):
        all_upload_files = UploadFile.objects.all()
        return render(request, 'file_show.html',{'all_upload_files':all_upload_files})

class FileDescView(View):
    def get(self, request):
        file_id = request.GET.get('file_id')
        try:
            file = UploadFile.objects.get(id=file_id)
            return render(request, 'file_detail.html', {'file': file})
        except UploadFile.DoesNotExist:
            return HttpResponse('别搞,没有这个文件')

class FileDownloadView(View):
    def get(self, request):
        file_name = request.GET.get('file_name')
        file_path = request.GET.get('file_path')
        save_path = '%s%s' % (settings.MEDIA_ROOT, file_path)
        f = open(save_path, 'rb')
        response = FileResponse(f)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename={}'.format(escape_uri_path(file_name))
        # f.close()  不能用
        return response

class RegisterView(View):
    def get(self, request):
        if request.user.is_authenticated():
            return HttpResponse('你已经在登录了,不给注册')
        else:
            return render(request, 'register.html')

    def post(self, request):
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if not all([username, password1, password2]):
            error = '数据不完整'
            return render(request, 'register.html', {'error': error})
        if password1 != password2:
            error = '密码不一致'
            return render(request, 'register.html', {'error': error})
        try:
            user = User.objects.get(username=username)
            error = '用户名已存在'
            return render(request, 'register.html', {'error': error})
        except User.DoesNotExist:
            # User.objects.create(username=username, password=password1)  # 密码没有加密
            User.objects.create_user(username=username, password=password1)  # 认证系统的
            return HttpResponse('注册成功')

class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated():
            return HttpResponse('你已经在登录了，不给登录')
        else:
            return render(request, 'login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not all([username, password]):
            error = '数据不完整'
            return render(request, 'login.html', {'error': error})
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', reverse('app_pic:index'))
            return redirect(next_url)
        else:
            error = '用户名或密码错误'
            return render(request, 'login.html',{'error': error})

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('app_pic:index'))