from django.contrib import admin


class ElementAdmin(admin.ModelAdmin):
    fields = ('version', 'code', 'value',)
    list_display = ('version', 'code', 'value',)
    list_display_links = ('version',)
    list_per_page = 15
    search_fields = ('version__num',)
    sortable_by = ('version', 'code', 'value',)
