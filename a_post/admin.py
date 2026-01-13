from django.contrib import admin
from .models import *
# Register your models here.

class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

admin.site.register(Post)
admin.site.register(LikedPost)

admin.site.register(Tag,TagAdmin)

admin.site.register(Comment)
admin.site.register(LikedComment)

admin.site.register(Reply)
admin.site.register(LikedReply)