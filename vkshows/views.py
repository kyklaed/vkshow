from django.shortcuts import render,redirect
from social_django.models import UserSocialAuth
import requests


def index(request):
    if str(request.user) == 'AnonymousUser':
        return render(request, 'vkshow/index.html')
    else:

        user = UserSocialAuth.objects.filter(user=request.user)
        extra = user.values('extra_data')[0]['extra_data']['access_token']
        uid = user.values('uid')
        r = requests.get('https://api.vk.com/method/getProfiles?access_token=%s&v=5.74' % (extra,))
        rr = requests.get('https://api.vk.com/method/friends.get?uid=%s&order=random&count=5&offset=100&'
                          'fields=city&name_case=nom&access_token=%s&v=5.74' % (uid, extra,))
        repos = []
        if r.status_code == 200 and rr.status_code == 200:
            name = r.json()['response'][0]['first_name'] + ' ' + r.json()['response'][0]['last_name']
            for i in rr.json()['response']['items']:
                repos.append(i['first_name'] + ' ' + i['last_name'])
            return render(request, 'vkshow/profile.html', {'name': name, 'repos': repos})

        return redirect('index')
