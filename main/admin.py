from django.contrib import admin

from main.model.refbook import Refbook
from main.model.version import Version
from main.model.element import Element
from main.adm.refbookadmin import RefbookAdmin
from main.adm.versionadmin import VersionAdmin
from main.adm.elementadmin import ElementAdmin

admin.site.register(Refbook, RefbookAdmin)
admin.site.register(Version, VersionAdmin)
admin.site.register(Element, ElementAdmin)
