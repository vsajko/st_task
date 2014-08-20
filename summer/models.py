from django.db import models


class Channel(models.Model):
    title = models.CharField(max_length=255, blank=True)
    link = models.CharField(max_length=255)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.title


class Items(models.Model):
    title = models.CharField(max_length=255)
    link = models.CharField(max_length=255)
    description = models.CharField(max_length=65535)
    guid = models.CharField(max_length=255)
    channel = models.ForeignKey(Channel)

    def __unicode__(self):
        return self.title


class Words(models.Model):
    word = models.CharField(max_length=128, unique=True)
    num = models.IntegerField()

    def __unicode__(self):
        return self.word


class WordsItems(models.Model):
    num = models.IntegerField()
    words = models.ForeignKey(Words)
    items = models.ForeignKey(Items)

    class Meta:
        unique_together = ('words', 'items')

    def __unicode__(self):
        return self.words.word + ' - ' + self.items.title


class WordsChannels(models.Model):
    num = models.IntegerField()
    words = models.ForeignKey(Words)
    channels = models.ForeignKey(Channel)

    class Meta:
        unique_together = ('words', 'channels')

    def __unicode__(self):
        return self.words.word + ' - ' + self.channels.title
