from django.contrib import admin

from watchhub.models import StreamPlatform,WatchContent,ContentReview

admin.site.register(StreamPlatform)
admin.site.register(WatchContent)
admin.site.register(ContentReview)

