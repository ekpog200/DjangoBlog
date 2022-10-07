import json

from django.contrib import admin
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder

from .models import *
# Register your models here.

class PostAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = Post
        fields = '__all__'



class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ("title",)}
    form = PostAdminForm
    save_on_top = True
    save_as = True
    list_display = ('id','title','slug','category','created_at','news_day','views','get_photo')
    list_display_links = ('id','title')
    search_fields = ('title',)
    list_filter = ('category', 'tags')
    readonly_fields = ('views','created_at','get_photo')
    fields = ('title','slug','category','tags','content','author','news_day','photo','get_photo','views','created_at')
    def get_photo(self,obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="50">')
        return '-'
    get_photo.short_description = 'Фото'

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ("title",)}
    list_display = ('id','title','slug')
    list_display_links = ('id','title')
    search_fields = ('title',)
    list_filter = ('title',)

class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ("title",)}
    list_filter = ('title',)
    list_display_links = ('id','title')
    list_display = ('id','title','slug')
    search_fields = ('title',)

admin.site.unregister(User)
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email','is_staff']

@admin.register(UserPlatformStats)
class StatUserAdmin(admin.ModelAdmin):
    def changelist_view(self, request, extra_context=None):

        stat_data = (
            UserPlatformStats.objects.annotate().values("win","mac","iphone","android","other")
        )

        # data = newstats.objects.all()
        # newdata = serializers.serialize('json', list(data), fields=("win","mac","iph","android","oth"))
        # print(newdata)

        as_json = json.dumps(list(stat_data), cls=DjangoJSONEncoder)
        extra_context = extra_context or {"stat_data": as_json}

        return super().changelist_view(request, extra_context=extra_context)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Post, PostAdmin)


