from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic.edit import CreateView

from django.conf import settings
from .models import IkiliCommitter, Ikili
import tweepy

from .models import Ikili
import requests


def index(request):
    ikili_list = []
    for ikili in Ikili.objects.get_top_ikili_list():
        try:
            html = requests.get(f'https://api.twitter.com/1/statuses/oembed.json?id={ikili.tweet_id}').json()['html']
            ikili_list.append({'html': html})
        except KeyError:
            pass
    return render(request, template_name='ikileaks_app/index.html', context={
        'ikili_list': ikili_list,
    })


class IkiliCreate(CreateView):
    model = Ikili
    fields = ['tweet_id']
    template_name = 'ikileaks_app/ikili_create.html'
    success_url = '/'


def twitter_login(request):
    consumer_token = settings.TWITTER_CLIENT_ID
    consumer_secret = settings.TWITTER_CLIENT_SECRET
    callback_url = settings.TWITTER_CALLBACK_URL

    auth = tweepy.OAuthHandler(consumer_key=consumer_token, consumer_secret=consumer_secret, callback=callback_url)
    url = auth.get_authorization_url()
    request.session['request_token'] = auth.request_token

    return redirect(url)


def twitter_callback(request):
    client_id = settings.TWITTER_CLIENT_ID
    client_secret = settings.TWITTER_CLIENT_SECRET

    auth = tweepy.OAuthHandler(client_id, client_secret)
    token = request.session.get('request_token')
    request.session.delete('request_token')

    auth.request_token = token

    try:
        auth.get_access_token(request.GET['oauth_verifier'])
    except tweepy.TweepError:
        print('Error! Failed to get access token.')

    api = tweepy.API(auth)
    twitter_id = api.get_user(auth.get_username()).id

    user = authenticate(username=twitter_id, password='')
    print('user', user)
    if user is not None:
        if user.is_active:
            login(request, user)
    else:
        print(IkiliCommitter.objects.all())
        user = IkiliCommitter.objects.create_user(twitter_id=twitter_id, password='')
        login(request, user)

    return redirect('/')
