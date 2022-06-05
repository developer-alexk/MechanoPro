from django.contrib import admin

from users.models import Account

admin.site.register(Account)

admin.site.site_header = 'Juakali B2C'
admin.site.site_title = 'Juakali B2C'
admin.site.index_title = 'Juakali B2C'
