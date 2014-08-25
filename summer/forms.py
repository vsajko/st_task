import sys
import pprint
from django import forms
from summer.models import Channel


class ChannelForm(forms.ModelForm):
    link = forms.URLField(label="Feed Url")

    class Meta:
        model = Channel


class WordsByFeed(forms.ModelForm):
    link = forms.ChoiceField()

    class Meta:
        model = Channel
