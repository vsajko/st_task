import sys
import pprint
import json
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from summer.models import Channel, Words, WordsItems, WordsChannels
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
            form.save()
            return list(request)
    else:
        form = ChannelForm()

    cxd['form'] = form

    return render_to_response('summer/add_channel.html', cxd, context)


def rijec(request):
    if request.method == 'GET':
        rijec = request.GET.get('rijec')
        feed_url = request.GET.get('feed_url')
        unos_url = request.GET.get('unos_url')
        rsp = find_rijec(rijec=rijec,
                         feed_url=feed_url,
                         unos_url=unos_url)
        return HttpResponse(json.dumps(rsp),
                            content_type="application/json")


def find_rijec(rijec=None, feed_url=None, unos_url=None):
    if not rijec:
        return {'error': '"rijec" mora biti zadana'}
    if unos_url and not feed_url:
        rsp = []
        # one url can be in multiple feeds
        results = WordsItems.objects.filter(words__word=rijec,
                                            items__link=unos_url)
        num = 0
        for res in results:
            num += res.num
            rsp.append({'num': res.num,
                        'feed_url': res.items.channel.link})

        return {'rijec': rijec, 'num': num, 'num_by_feed': rsp}
    elif feed_url and not unos_url:
        rsp = []
        # one url can be in multiple items
        results = WordsItems.objects.filter(words__word=rijec,
                                            items__channel__link=feed_url)
        num = 0
        for res in results:
            num += res.num
            rsp.append({'num': res.num,
                        'unos_url': res.items.link})

        return {'rijec': rijec, 'num': num, 'num_by_unos': rsp}
    elif unos_url and feed_url:
        # this should be unique
        try:
            res = WordsItems.objects.get(words__word=rijec,
                                         items__link=unos_url,
                                         items__channel__link=feed_url)
        except ObjectDoesNotExist:
            return {'error': 'rijec: "%s" nije u bazi' % rijec}
        except MultipleObjectsReturned:
            return {'error': 'rijec: "%s" data integrity error' % rijec}

        return {'rijec': rijec,
                'num': res.num,
                'feed_url': feed_url,
                'unos_url': unos_url}

    else:
        try:
            res = Words.objects.get(word=rijec)
        except ObjectDoesNotExist:
            return {'error': 'rijec: "%s" nije u bazi' % rijec}

    return {'rijec': rijec,
            'num': res.num}

