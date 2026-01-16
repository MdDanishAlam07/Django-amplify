from urllib import request
from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from .models import Tweet, Like, ContactMessage
from .forms import TweetForm, UserRegisterForm
from django.shortcuts import  get_object_or_404, redirect
from django.contrib.auth import login
from django.db.models import Q
# Create your views here.
def index(request):
    return render(request, 'index.html')




def contact(request):
    return render(request, "contact.html")


def contact(request):
    if request.method == "POST":
        ContactMessage.objects.create(
            name=request.POST.get("name"),
            email=request.POST.get("email"),
            message=request.POST.get("message"),
        )
        return render(request, "contact.html", {"success": True})

    return render(request, "contact.html")


def tweet_list(request):
    query = request.GET.get('q')

    if query:
        tweets = Tweet.objects.filter(
            Q(text__icontains=query) |
            Q(user__username__icontains=query)
        ).order_by('-created_at')
    else:
        tweets = Tweet.objects.all().order_by('-created_at')

    return render(request, 'tweet_list.html', {'tweets': tweets})


@login_required
def tweet_create(request):
    if request.method == 'POST':
         form = TweetForm(request.POST, request.FILES)
         if form.is_valid():
                tweet = form.save(commit=False)
                tweet.user = request.user
                tweet.save()
                return redirect('tweet_list')
    else:
        form = TweetForm()
    return render(request, 'tweet_form.html', {'form': form})

@login_required
def tweet_edit(request,tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id,user=request.user)
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES, instance=tweet)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('tweet_list')
    else:
        form = TweetForm(instance=tweet)
    return render(request, 'tweet_form.html', {'form': form, 'tweet': tweet})  


@login_required
def tweet_delete(request, tweet_id):
     tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)
     if request.method == 'POST':
        tweet.delete()
        return redirect('tweet_list')
     return render(request, 'tweet_confirm_delete.html', {'tweet': tweet})



def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
          user =  form.save(commit=False)
          user.set_password(form.cleaned_data['password1'])
          user.save()
          login(request, user)
          return redirect('tweet_list')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def like_tweet(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id)

    like, created = Like.objects.get_or_create(
        user=request.user,
        tweet=tweet
    )

    if not created:
        like.delete()  # unlike

    return redirect('tweet_list')