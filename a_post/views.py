from django.shortcuts import render,redirect, get_object_or_404
from .models import Post, Tag, Comment, Reply
from .forms import PostCreateForm, CommentCreateForm, ReplyCreateForm
from django.contrib import messages
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.db.models import Count
from django.contrib.auth.decorators import login_required

# Create your views here.

def home_view(request, tag=None):
    if tag:
        posts = Post.objects.filter(tags__slug = tag)
        tag = get_object_or_404(Tag, slug=tag)
    else:
        posts = Post.objects.all()

    paginator = Paginator(posts,3)
    page = int(request.GET.get('page',1))
    try:
        posts = paginator.page(page)
    except:
        return HttpResponse('')
    
    context = {
        'posts': posts,   
        'tag':tag,
        'page':page,
    }
    if request.htmx:
        return render(request, 'snippets/loop_home_posts.html', context)
    return render(request, 'a_post/home.html',context)

@login_required
def post_create_view(request):
    if request.method =='POST':
        form = PostCreateForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')
    else:
        form = PostCreateForm()
    context = {
        'form': form
    }   
    return render(request, 'a_post/post_create.html',context)

@login_required
def post_delete_view(request,pk):
    post = get_object_or_404(Post, id=pk, author=request.user)
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post delted successfully.')
        return redirect('home')
    context = {
        'post':post,
    }
    return render(request, 'a_post/post_delete.html', context)

@login_required
def post_edit_view(request,pk):
    post = get_object_or_404(Post, id=pk, author=request.user)
    if request.method == 'POST':
        form = PostCreateForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = PostCreateForm(instance=post)
    context = {
        'post':post,
        'form':form,
    }
    return render(request, 'a_post/post_edit.html',context)


def post_page_view(request, pk):
    post = get_object_or_404(Post, id=pk)
    commentForm = CommentCreateForm()
    replyForm = ReplyCreateForm()
    

    if request.htmx:
        if 'top' in request.GET:
            # comments = post.comments.filter(likes__isnull=False).distinct()
            comments = post.comments.annotate(num_likes=Count('likes')).filter(num_likes__gt=0).order_by('-num_likes')
        else:
            comments = post.comments.all()
        return render(request, 'snippets/loop_postpage_comments.html', {'comments':comments,'replyform':replyForm,})
    context = {
        'post':post,
        'commentForm':commentForm,
        'replyform':replyForm,
    }
    return render(request, 'a_post/post_page.html',context)

@login_required
def comment_sent(request, pk):
    post = get_object_or_404(Post, id=pk)
    replyform = ReplyCreateForm()
    if request.method == 'POST':
        form = CommentCreateForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.parent_post = post
            comment.save()
    context = {
        'comment':comment,
        'post':post,
        'replyform':replyform
    }
    return render(request,'snippets/add_comment.html',context)

@login_required
def comment_delete_view(request,pk):
    post = get_object_or_404(Comment, id=pk, author=request.user)
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Comment delted successfully.')
        return redirect('post', post.parent_post.id)
    context = {
        'comment':post,
    }
    return render(request, 'a_post/comment_delete.html', context)

def reply_sent(request, pk):
    comment = get_object_or_404(Comment, id=pk)
    replyform = ReplyCreateForm()
    if request.method == 'POST':
        form = ReplyCreateForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.author = request.user
            reply.parent_comment = comment
            reply.save()
    context = {
        'comment':comment,
        'reply':reply,
        'replyform':replyform
    }
    return render(request, 'snippets/add_reply.html', context)

@login_required
def reply_delete_view(request,pk):
    reply = get_object_or_404(Reply, id=pk, author=request.user)
    if request.method == 'POST':
        reply.delete()
        messages.success(request, 'Reply delted successfully.')
        return redirect('post', reply.parent_comment.parent_post.id)
    context = {
        'reply':reply,
    }
    return render(request, 'a_post/reply_delete.html', context)

def like_toggle(model):
    def inner_func(func):
        def wrapper(request, *args, **kwargs):
            post = get_object_or_404(model, id=kwargs.get('pk'))
            user_exist = post.likes.filter(username=request.user.username).exists()
            if post.author != request.user:
                if user_exist:
                    post.likes.remove(request.user)
                else:
                    post.likes.add(request.user)
            return func(request, post)
        return wrapper
    return inner_func

@login_required
@like_toggle(Post)
def like_post(request, post):
    return render(request, 'snippets/likes.html', {'post':post})

@login_required
@like_toggle(Comment)
def like_comment(request, comment):
    return render(request, 'snippets/likes_comment.html', {'comment':comment})
    
@login_required
@like_toggle(Reply)
def like_reply(request, reply):
    return render(request, 'snippets/likes_reply.html', {'reply':reply})
    
