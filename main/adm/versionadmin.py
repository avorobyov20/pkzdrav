from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import AdminDateWidget
from django.utils.safestring import mark_safe
from main.model.element import Element


class VersionAdminForm(forms.ModelForm):
    date_start = forms.DateField(widget=AdminDateWidget(),
                                 label='Дата начала действия',
                                 )


class ElementInline(admin.TabularInline):
    model = Element


class VersionAdmin(admin.ModelAdmin):
    list_display = ('refbook', 'num_', 'date_start_', 'cnt_')
    list_per_page = 15
    inlines = (ElementInline,)
    search_fields = ('refbook__code', )
    form = VersionAdminForm

    def num_(self, obj):
        return mark_safe('<a href="/admin/main/element/?q=' + obj.num + '">' + obj.num + '</a>')
    num_.short_description = 'Номер версии (фильтр)'
    num_.admin_order_field = 'num'

    def date_start_(self, obj):
        href = '/refbooks/?date=' + obj.date_start.strftime('%Y-%m-%d')
        return mark_safe('<a href="' + href + '" target="_blank">' + href + '</a>')
    date_start_.short_description = 'Действует с…'
    date_start_.admin_order_field = 'date_start'

    def cnt_(self, obj):
        return mark_safe(
            '<a href="/refbooks/' + str(obj.refbook.pk) + '/elements?version=' + str(obj.num) + '" target="_blank">' +
            str(obj.element_set.count()) + '&nbsp;&nbsp;&nbsp;/elements?version=' + str(obj.num) + '</a>'
        )
    cnt_.short_description = 'Количество элементов'
