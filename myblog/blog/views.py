from django.shortcuts import render, redirect, HttpResponse, get_object_or_404, HttpResponseRedirect
from .models import Post, Blog, Like
from django.contrib.auth.models import User
import markdown
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
import json
from .forms import CommentForm, PostForm

def BlogList(request):
    blogs = Blog.objects.all()
    return render(request, 'blogsindex.html', {'home': blogs})

def PostList(request, slug):
    blog = get_object_or_404(Blog, Slug=slug)    
    tag = request.GET.get('tag')
    posts = Post.objects.all().filter(blog_id=slug)
    if  tag and tag != None:
        posts = posts.filter(tags__name__in=[tag])
    # get_object_or_404(Blog, Slug=slug)
    return render(request, 'index.html', 
            {'post_list': posts,
            'blog': blog,
            'tag': tag}
            )

def PostDetail(request, slug):
    template_name = 'post_detail.html'
    post = get_object_or_404(Post, Slug=slug)
    
    post.comment = markdown.markdown(post.Content,
        extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
        ])
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()
   
    return render(request, template_name, {'post': post,                                          
                                           'comments': comments,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form})


@login_required(login_url='/userprofile/login/')
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if  form.is_valid():
            post = form.save(commit=False)
            post.Author = request.user
            #post.published_date = timezone.now()
            post.save()
            form.save_m2m()
            return redirect("blog:home")
        else:
            return HttpResponse("Что-то пошло не так")
    else:
        post_form = PostForm()
        columns = Blog.objects.all()
        context = { 'article_post_form': post_form, 'columns': columns }
        return render(request, 'create.html', context)                                       



@login_required
def postpreference(request, postid, userpreference):        
        if request.method == "POST":
                post= get_object_or_404(Post, id=postid)
                obj=''
                valueobj=''
                try:
                        obj= Like.objects.get(user= request.user, post= post)
                        valueobj= obj.value #value of userpreference
                        valueobj= int(valueobj)
                        userpreference= int(userpreference)                
                        if valueobj != userpreference:
                                obj.delete()
                                upref= Like()
                                upref.user= request.user
                                upref.post= post
                                upref.value= userpreference
                                if userpreference == 1 and valueobj != 1:
                                        post.likes += 1
                                        post.dislikes -=1
                                elif userpreference == 2 and valueobj != 2:
                                        post.dislikes += 1
                                        post.likes -= 1                                
                                upref.save()
                                post.save()                                                
                                context= {'eachpost': post,
                                  'postid': postid}
                                post.comment = markdown.markdown(post.Content,
                                extensions=[
                                        'markdown.extensions.extra',
                                        'markdown.extensions.codehilite',
                                ])
                                comments = post.comments.filter(active=True)
                                new_comment = None        
                                comment_form = CommentForm()                
                                context= {'post': post,
                                            'postid': postid,
                                            'comments': comments,
                                            'new_comment': new_comment,
                                            'comment_form': comment_form
                                            }
                                return render (request, 'post_detail.html', context)

                        elif valueobj == userpreference:
                                obj.delete()                        
                                if userpreference == 1:
                                        post.likes -= 1
                                elif userpreference == 2:
                                        post.dislikes -= 1
                                post.save()
                                post.comment = markdown.markdown(post.Content,
                                extensions=[
                                        'markdown.extensions.extra',
                                        'markdown.extensions.codehilite',
                                ])
                                comments = post.comments.filter(active=True)
                                new_comment = None        
                                comment_form = CommentForm()                
                                context= {'post': post,
                                            'postid': postid,
                                            'comments': comments,
                                            'new_comment': new_comment,
                                            'comment_form': comment_form
                                            }
                                return render (request, 'post_detail.html', context)                                                                                
                except Like.DoesNotExist:
                        upref= Like()
                        upref.user= request.user
                        upref.post= post
                        upref.value= userpreference

                        userpreference= int(userpreference)

                        if userpreference == 1:
                                post.likes += 1
                        elif userpreference == 2:
                                post.dislikes +=1
                        upref.save()
                        post.save()                            
                        post.comment = markdown.markdown(post.Content,
                        extensions=[
                                'markdown.extensions.extra',
                                'markdown.extensions.codehilite',
                        ])
                        comments = post.comments.filter(active=True)
                        new_comment = None        
                        comment_form = CommentForm()                
                        context= {'post': post,
                                    'postid': postid,
                                    'comments': comments,
                                    'new_comment': new_comment,
                                    'comment_form': comment_form
                                    }
                        return render (request, 'post_detail.html', context)
        else:
            post= get_object_or_404(Post, id=postid)
            post.comment = markdown.markdown(post.Content,
            extensions=[
                    'markdown.extensions.extra',
                    'markdown.extensions.codehilite',
            ])
            comments = post.comments.filter(active=True)
            new_comment = None        
            comment_form = CommentForm()                
            context= {'post': post,
                        'postid': postid,
                        'comments': comments,
                        'new_comment': new_comment,
                        'comment_form': comment_form
                        }
            return render (request, 'post_detail.html', context)


@login_required(login_url='/userprofile/login/')
def post_update(request, id):
    post = Post.objects.get(id=id)

    if request.user != post.Author:
        return HttpResponse("error")

    if request.method == "POST":
        post_form = PostForm(data=request.POST)
        if post_form.is_valid():
                        
            post.Title = request.POST['Title']
            post.Content = request.POST['Content']       
            
            post.tags.set(*request.POST.get('tags').split(','), clear=True)
            post.save()
            return redirect("blog:post_detail", slug=post.Slug)
        else:
            return HttpResponse("Что-то пошло не так")

    else:
        post_form = PostForm()
        
        blogs = Blog.objects.all()
        context = { 'article_post_form': post_form,
                    'post': post,
                    'blogs': blogs }

        return render(request, 'update.html', context)            