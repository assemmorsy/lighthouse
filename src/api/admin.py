from django.contrib import admin
from .models import (
    UnKnownMissingPerson,
    KnownMissingPerson,
    KnownMissingPersonTrackRecord,
    UnknownMissingPersonTrackRecord,
    KnownMissingPersonImages,User,Quereies)

admin.site.register(UnKnownMissingPerson)
admin.site.register(KnownMissingPerson)
admin.site.register(UnknownMissingPersonTrackRecord)
admin.site.register(KnownMissingPersonTrackRecord)
admin.site.register(KnownMissingPersonImages)
admin.site.register(User)
admin.site.register(Quereies)
