from django.contrib import admin
from django.utils.safestring import mark_safe
from main.model.version import Version


class VersionInline(admin.TabularInline):
    model = Version


class RefbookAdmin(admin.ModelAdmin):
    fields = ('code', 'name', 'description',)
    list_display = ('code', 'name', 'description', 'cnt_')
    list_display_links = ('code', 'cnt_')
    list_per_page = 8
    inlines = (VersionInline,)
    search_fields = ('code',)
    sortable_by = ()

    def cnt_(self, obj):
        return mark_safe('<a href="/admin/main/version/?q=' + obj.code + '">' + str(obj.version_set.count()) + '</a>')
    cnt_.short_description = 'Количество версий (фильтр)'
