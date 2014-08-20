from django.contrib import admin
# Register your models here.
from summer.models import(Channel,
                          Items,
                          Words,
                          WordsItems,
                          WordsChannels)


admin.site.register(Channel)
admin.site.register(Items)
admin.site.register(Words)
admin.site.register(WordsItems)
admin.site.register(WordsChannels)
