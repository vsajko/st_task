import sys
import pprint
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from summer.models import Channel
from summer.forms import ChannelForm


def index(request):
    context = RequestContext(request)
    cxd = {}

    return render_to_response('summer/index.html', cxd, context)


def list(request):
    context = RequestContext(request)
    cxd = {}
    channels = Channel.objects.all()
    cxd['channels'] = channels

    return render_to_response('summer/list.html', cxd, context)


def add_channel(request):
    context = RequestContext(request)
    cxd = {}
    if request.method == 'POST':
        form = ChannelForm(request.POST)
        if form.is_valid():
            channel = form.save()
            return list(request)
    else:
        form = ChannelForm()

    cxd['form'] = form

    return render_to_response('summer/add_channel.html', cxd, context)
