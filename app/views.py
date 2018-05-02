from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import json


def index(request):
    return render(request, 'app/description.html', {})



@login_required(login_url="/oauth/login/twitter/")
def twitter_report(request):
    return render(request, 'app/twitter-report.html', {})


