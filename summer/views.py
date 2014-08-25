import sys
import pprint
import json
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from summer.models import Channel, Words, WordsItems, WordsChannels
from summer.forms import ChannelForm


def index(request):
    """ nothing here empty index page
    """
    context = RequestContext(request)
    cxd = {}

    return render_to_response('summer/index.html', cxd, context)


def list(request):
    """ show list of feeds
    """
    context = RequestContext(request)
    cxd = {}
    channels = Channel.objects.all()
    cxd['channels'] = channels

    return render_to_response('summer/list.html', cxd, context)


def add_channel(request):
    """ add new feed
    """
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


def toplist(request):
    """ show top list of words by number of occurences
        can be filtered by feed
    """
    context = RequestContext(request)
    cxd = {}
    feedlink = request.GET.get('feedlink')
    if feedlink:
        words = WordsChannels.objects.filter(
            channels__link=feedlink
        ).order_by('-num').values_list('words__word', 'num')
    else:
        words = Words.objects.order_by('-num').values_list('word', 'num')

    feeds = Channel.objects.order_by('link')
    paginator = Paginator(words, 10)
    page = request.GET.get('page')
    try:
        paged = paginator.page(page)
    except PageNotAnInteger:
        paged = paginator.page(1)
    except EmptyPage:
        paged = paginator.page(paginator.num_pages)

    cxd['words'] = paged
    cxd['feedlink'] = feedlink
    cxd['feeds'] = feeds

    return render_to_response('summer/toplist.html', cxd, context)


def change_feed_status(request):
    """ changes status of feed active/inactive
        ajax request
    """
    if request.method == 'GET':
        feedid = request.GET.get('feedid')
        if feedid:
            try:
                channel = Channel.objects.get(id=feedid)
                if channel.active:
                    channel.active = False
                else:
                    channel.active = True
                channel.save()
            except:
                return redirect('/summer/list/')
            return HttpResponse(channel.active)

    return redirect('/summer/list/')


def rijec(request):
    """ json api response for
        word requests

    get params
        rijec: required - wanted word
        feed_url: url of wanted feed
        unos_url: url of feed item

    result is unique if only 'rijec' is in request
    or all 3 params are in request

    example responses:
    GET
    http://localhost:8000/summer/rijec/?rijec=the&unos_url=http://danielpocock.com/getting-selected-for-google-summer-of-code-2015
    { num_by_feed: [ { num: 181, feed_url: "http://planet.debian.org/rss20.xml" } ],
    num: 181,
    rijec: "the"
    }

    GET
    http://localhost:8000/summer/rijec/?rijec=the&feed_url=http://planet.debian.org/rss20.xml
    {
    num_by_unos: [
    {
    num: 6,
    unos_url: "http://info.comodo.priv.at/blog/debian_perl_group_micro_sprint.html"
    },
    .....
    {
    num: 14,
    unos_url: "http://www.eyrie.org/~eagle/journal/2014-08/002.html"
    }
    ],
    num: 1674,
    rijec: "the"
    }

    GET
    http://localhost:8000/summer/rijec/?rijec=the&feed_url=http://planet.debian.org/rss20.xml&unos_url=http://danielpocock.com/getting-selected-for-google-summer-of-code-2015
    {
    num: 181,
    feed_url: "http://planet.debian.org/rss20.xml",
    rijec: "the",
    unos_url: "http://danielpocock.com/getting-selected-for-google-summer-of-code-2015"
    }

    GET
    http://localhost:8000/summer/rijec/?rijec=the
    {
    num: 4588,
    rijec: "the"
    }
    """
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
    """ helper for JSON api /rijec/
    """
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

        return {'rijec': rijec,
                'num': num,
                'num_by_feed': rsp,
                'unos_url': unos_url }

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

        return {'rijec': rijec,
                'num': num,
                'num_by_unos': rsp,
                'feed_url': feed_url}

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


