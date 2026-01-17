from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile
from a_post.forms import ReplyCreateForm
from django.http import Http404
from django.contrib.auth.models import User
from .forms import ProfileForm
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db.models import Count
from allauth.account.models import EmailAddress

# Create your views here.

def profile_view(request, username=None):
    if username:
        profile = get_object_or_404(User, username=username).profile
    else:
        try:
            profile = request.user.profile
        except: 
            raise Http404("Profile does not exist.")
    posts = profile.user.posts.all()
    replyform = ReplyCreateForm()
    if request.htmx:
        if 'top-posts' in request.GET:
            posts = profile.user.posts.annotate(num_likes=Count('likes')).filter(num_likes__gt=0).order_by('-num_likes')
            
        elif 'top-comments' in request.GET:
            comments = profile.user.comments.annotate(num_likes=Count('likes')).filter(num_likes__gt=0).order_by('-num_likes')
            return render(request, 'snippets/loop_profile_comments.html',{'comments':comments,'replyform':replyform,})
        elif 'liked-posts' in request.GET:
            posts = profile.user.likedposts.order_by('-likedpost__created_at')
            
        return render(request, 'snippets/loop_profile_posts.html',{'posts':posts})

    context = {
        'profile': profile,
        'posts':posts,
    }
    return render(request, 'a_users/profile.html', context)

@login_required
def profile_edit_view(request):
    form = ProfileForm(instance=request.user.profile)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()

            if request.user.emailaddress_set.get(primary=True).verified:       
                return redirect('profile')
            else:
                return redirect('profile-verify-email')
    
    if request.path == reverse('profile-onboarding'):
        template = 'a_users/profile_onboarding.html'
    else:
        template = 'a_users/profile_edit.html'
    return render(request, template, {'form': form})

@login_required
def profile_delete_view(request):
    user = request.user
    if request.method == "POST":
        logout(request)
        user.delete()
        messages.success(request, 'Account deleted successfully.')
        return redirect('home')
    return render(request, 'a_users/profile_delete.html')
    
@login_required
def profile_verify_email(request):
    email = request.user.email

    if not email:
        messages.error(request, "No email address found.")
        return redirect('profile')

    email_address, created = EmailAddress.objects.get_or_create(
        user=request.user,
        email=email,
        defaults={'primary': True}
    )

    if not email_address.verified:
        email_address.send_confirmation(request)
        messages.success(request, "Verification email sent. Check your inbox.")
    else:
        messages.info(request, "Your email is already verified.")

    return redirect('profile')
