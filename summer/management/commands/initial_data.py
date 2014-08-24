import sys
from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from summer.models import Channel
from django.db import transaction

word_min_len = 3


class Command(BaseCommand):
    args = 'nothing'
    help = 'fills channel table with some initial feeds'



    def handle(self, *args, **options):
        channels = (
            {'title': 'BBc world',
             'link': 'http://feeds.bbci.co.uk/news/world/rss.xml'},
            {'title': 'Ars Technica',
             'link': 'http://feeds.arstechnica.com/arstechnica/index/'},
            {'title': 'net.hr',
             'link': 'http://www.net.hr/rss/feeds/naslovnica/index.xml'},
            {'title': 'planet debian',
             'link': 'http://planet.debian.org/rss20.xml'},
            {'title': 'perlsphere',
             'link': 'http://perlsphere.net/rss.xml'},
            {'title': 'planet python',
             'link': 'http://planet.python.org/rss20.xml'},
            {'title': 'sarajevo.ba',
             'link': 'http://sarajevo.ba/danes_frontengine/rss/rss.php?siteid=1'},
            {'title': 'netokracija comments',
             'link': 'http://www.netokracija.com/comments/feed'},
            {'title': 'netokracija',
             'link': 'http://feeds.netokracija.com/netokracija'},
            {'title': 'github shougo',
             'link': 'https://github.com/Shougo.atom'},
            {'title': 'The Guardian',
             'link': 'http://feeds.theguardian.com/theguardian/uk/rss'},
            {'title': 'Novi List 404 :)',
             'link': 'http://www.novilist.hr/rss/feed/sve.xml'},
            {'title': 'Reddit',
             'link': 'http://www.reddit.com/.rss'},
            {'title': 'Top Stories - Google News',
             'link': 'https://news.google.com/news/feeds?pz=1&cf=all&ned=us&hl=en&topic=h&num=3&output=rss'},
            {'title': 'Slashdot',
             'link': 'http://rss.slashdot.org/Slashdot/slashdot'},
            {'title': 'Hacker News',
             'link': 'https://news.ycombinator.com/rss'},
            {'title': 'newest submissions : reddit.com',
             'link': 'http://www.reddit.com/new/.rss'},
            {'title': '24sata',
             'link': 'http://www.24sata.hr/feeds/najnovije.xml'},
            {'title': 'hrt',
             'link': 'http://www.hrt.hr/rss/vijesti/'},
        )
        self.fill_channels(channels)


    @transaction.atomic
    def fill_channels(self, channels):
        for ch in channels:
            summer_channel, _ = Channel.objects.get_or_create(link=ch['link'])
            if 'title' in ch:
                summer_channel.title = ch['title']
            summer_channel.save()




