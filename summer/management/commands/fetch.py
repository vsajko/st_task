import re
import sys
from datetime import datetime
import pytz
import hashlib
from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from summer.models import Channel, Items, Words, WordsChannels, WordsItems
import feedparser
from bs4 import BeautifulSoup
from django.db import transaction

word_min_len = 3


class Command(BaseCommand):
    args = 'nothing'
    help = 'fetches and saves feeds'

    option_list = BaseCommand.option_list + (
        make_option('--link',
                    action='store',
                    type='string',
                    dest='link',
                    help='Process feed from link instead of ones from db. '
                    'Feed will be saved to db'
                    'active will be set to true if fedd is fetchable'),
        make_option('--wordlen',
                    action='store',
                    type='int',
                    dest='wordlen',
                    default=2,
                    help='words must have more than this characters to be counted'
                    ),
        make_option('--forcefetch',
                    action='store_true',
                    dest='forcefetch',
                    default=False,
                    help='process feed without checking etag and modified headers'
                    ),
    )

    def handle(self, *args, **options):
        self.stdout.write("-----------")
        self.options = options
        if 'link' in options and options['link'] is not None:
            self.proc_channel(options['link'])
        else:
            channels = Channel.objects.filter(active=True)
            for ch in channels:
                self.stdout.write("-----------")
                self.stdout.write('from db: %s' % ch.link)
                self.proc_channel(ch.link)


    def proc_channel(self, link):
        self.stdout.write("feed_url: %s" % link)
        channel, _ = Channel.objects.get_or_create(link=link)

        if self.options.get('forcefetch', False):
            feed = feedparser.parse(link)
        else:
            feed = feedparser.parse(link,
                                    modified=channel.last_modified,
                                    etag=channel.etag)

        # FIXME
        # thoretically we should check http status here but
        # there is interesting case of Novi List which returns
        # status 404 and regular content ?!?!
        # also net.hr redirects to other url and this is not visible in
        # feedparser headers
        # maybe we should first fetch feed with urllib2?

        if len(feed.feed.keys()) < 1:
            self.stdout.write('empty feed or no changes')
        else:
            # update title in table
            if 'title' in feed.feed:
                self.stdout.write(feed.feed.title)
                channel.title = feed.feed.title
            else:
                self.stdout.write('can not parse title')

            if 'etag' in feed:
                self.stdout.write("etag: %s" % feed.etag)
                channel.etag = feed.etag
            if 'modified' in feed:
                channel.last_modified = self.date_with_tz(feed.modified_parsed)

            channel.active = True
            channel.save()
            self.proc_feed(feed, channel)



    @transaction.atomic
    def proc_feed(self, feed, channel):
        # we will take words from title and summary
        if 'entries' in feed:
            for entry in feed.entries:
                title_words = []
                summary_words = []
                content_words = []
                if 'id' in entry:
                    item_id = entry.id
                else:
                    item_id = self.make_hash(str(entry))

                item, created = Items.objects.get_or_create(channel=channel,
                                                            guid=item_id)
                if created:
                    if 'title' in entry:
                        title_words = self.get_words(entry.title)
                        item.title = entry.title
                    if 'summary' in entry:
                        summary_words = self.get_words(entry.summary)
                    if 'content' in entry:
                        for cnt in entry.content:
                            if 'value' in cnt:
                                content_words.extend(
                                    self.get_words(cnt['value']))
                    # FIXME what to do with tags?
                    # if 'tags' in entry:
                    #     self.stdout.write("tags: %s" % entry.tags)

                    # content is usually longer and with richer formatting
                    # if there are both content and summary present
                    # we will take longer of them
                    if len(content_words) > len(summary_words):
                        words = title_words + content_words
                    else:
                        words = title_words + summary_words

                    self.save_words(words, channel, item)
                    item.save()
                else:
                    self.stdout.write('no new entries')

        else:
            self.stdout.write('no entries')

    def get_words(self, val):
        # regex for all non word characters
        wre = re.compile(ur"[\W_0-9]+", re.UNICODE)

        soup = BeautifulSoup(val)

        # get text from val and lowercase it
        text_low = soup.get_text().lower()
        # replace all non word characters with space
        text_clean = wre.sub(' ', text_low)
        # get words from text with more chars than wordlen
        words = filter(lambda x: len(x) > self.options.get('wordlen', 0),
                       text_clean.split())
        return words


    @transaction.atomic
    def save_words(self, words, channel, item):
        # words_dict = {}
        for word in words:
            # self.stdout.write("word:  %s" % word)
            # words_dict['word']
            db_word, _ = Words.objects.get_or_create(word=word)
            db_word.num += 1
            db_word.save()

            wordschannel, _ = WordsChannels.objects.get_or_create(
                words=db_word,
                channels=channel)
            wordschannel.num += 1
            wordschannel.save()

            wordsitems, _ = WordsItems.objects.get_or_create(
                words=db_word,
                items=item)
            wordsitems.num += 1
            wordsitems.save()


    def date_with_tz(self, time_tuple):
        """ converts time tuple to datetime and assigns UTC timezone

            sqlite does not save timezone info but django by default
            expects timezone aware datetime

        :param time_tuple: time tuple
        :returns: datetime string with utc timezone
        :rtype: string
        """
        date_tmp = datetime(*time_tuple[:5])
        utc = pytz.utc
        return utc.localize(date_tmp).isoformat()

    def make_hash(self, str):
        return hashlib.md5(str).hexdigest()


