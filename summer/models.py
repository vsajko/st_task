from django.db import models


class Channel(models.Model):
    title = models.CharField(max_length=1024, blank=True, null=True, editable=False)
    link = models.CharField(max_length=1024, unique=True)
    active = models.BooleanField(default=True)
    etag = models.CharField(max_length=255, blank=True, null=True, editable=False)
    last_modified = models.DateTimeField(blank=True, null=True, editable=False)

    def __unicode__(self):
        return self.link


class Items(models.Model):
    channel = models.ForeignKey(Channel)
    title = models.CharField(max_length=1024, blank=True, null=True)
    link = models.CharField(max_length=1024, blank=True, null=True)

    class Meta:
        unique_together = ('channel', 'link')

    def __unicode__(self):
        return self.link


class Words(models.Model):
    word = models.CharField(max_length=128, unique=True)
    num = models.IntegerField(default=0)

    def __unicode__(self):
        return self.word


class WordsItems(models.Model):
    num = models.IntegerField(default=0)
    words = models.ForeignKey(Words)
    items = models.ForeignKey(Items)

    class Meta:
        unique_together = ('words', 'items')

    def __unicode__(self):
        return self.words.word + ' - ' + self.items.link


class WordsChannels(models.Model):
    num = models.IntegerField(default=0)
    words = models.ForeignKey(Words)
    channels = models.ForeignKey(Channel)

    class Meta:
        unique_together = ('words', 'channels')

    def __unicode__(self):
        return self.words.word + ' - ' + self.channels.link
