from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .forms import UserLoginForm, UserRegisterForm

from .forms import ProfileForm
from .models import Profile


# Create your views here.

def user_login(request):
    if request.method == 'POST':
        user_login_form = UserLoginForm(data=request.POST)
        if user_login_form.is_valid():
            data = user_login_form.cleaned_data
            user = authenticate(username=data['username'], password=data['password'])
            if user:
                login(request, user)
                return redirect("blog:home")
            else:
                return HttpResponse("Smth is wrong")
        else:
            return HttpResponse("Smth is wrong here")
    elif request.method == 'GET':
        user_login_form = UserLoginForm()
        context = { 'form': user_login_form }
        return render(request, 'login.html', context)
    else:
        return HttpResponse("Smth is wrong with GET")


def user_logout(request):
    logout(request)
    return redirect("blog:home")


def user_register(request):
    if request.method == 'POST':
        user_register_form = UserRegisterForm(data=request.POST)
        if user_register_form.is_valid():
            new_user = user_register_form.save(commit=False)
            new_user.set_password(user_register_form.cleaned_data['password'])
            new_user.save()
            login(request, new_user)
            return redirect("blog:home")
        else:
            return HttpResponse("注册表单输入有误。请重新输入~")
    elif request.method == 'GET':
        user_register_form = UserRegisterForm()
        context = { 'form': user_register_form }
        return render(request, 'register.html', context)
    else:
        return HttpResponse("请使用GET或POST请求数据")



@login_required(login_url='/userprofile/login/')
def user_delete(request, id):
    if request.method == 'POST':
        user = User.objects.get(id=id)
        if request.user == user:
            logout(request)
            user.delete()
            return redirect("blog:home")
        else:
            return HttpResponse("你没有删除操作的权限。")
    else:
        return HttpResponse("仅接受post请求。")


# # 编辑用户信息
# @login_required(login_url='/userprofile/login/')
# def profile_edit(request, id):
#     user = User.objects.get(id=id)

#     # 旧教程代码
#     # profile = Profile.objects.get(user_id=id)
#     # 新教程代码： 获取 Profile
#     if Profile.objects.filter(user_id=id).exists():
#         # user_id 是 OneToOneField 自动生成的字段
#         profile = Profile.objects.get(user_id=id)
#     else:
#         profile = Profile.objects.create(user=user)


#     if request.method == 'POST':
#         # 验证修改数据者，是否为用户本人
#         if request.user != user:
#             return HttpResponse("你没有权限修改此用户信息。")

#         # 上传的文件保存在 request.FILES 中，通过参数传递给表单类
#         profile_form = ProfileForm(request.POST, request.FILES)

#         if profile_form.is_valid():
#             # 取得清洗后的合法数据
#             profile_cd = profile_form.cleaned_data

#             profile.email = profile_cd['email']
#             profile.bio = profile_cd['bio']

#             # 如果 request.FILES 存在文件，则保存
#             if 'photo' in request.FILES:
#                 profile.photo = profile_cd["photo"]

#             profile.save()
#             # 带参数的 redirect()
#             return redirect("userprofile:edit", id=id)
#         else:
#             return HttpResponse("注册表单输入有误。请重新输入~")

#     elif request.method == 'GET':
#         profile_form = ProfileForm()
#         context = { 'profile_form': profile_form, 'profile': profile, 'user': user }
#         return render(request, 'edit.html', context)
#     else:
#         return HttpResponse("请使用GET或POST请求数据")