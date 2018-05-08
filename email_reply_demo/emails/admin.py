from django.contrib import admin
from .models import EmailMessage, EmailHeader, ReceivedEmailMessage


class EmailMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'created', 'subject', 'recipient_email_address',
                    'sending_status', 'resend_count')


class EmailHeaderAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'value')


class ReceivedEmailMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'subject', 'sender_email_address')


admin.site.register(EmailMessage, EmailMessageAdmin)
admin.site.register(EmailHeader, EmailHeaderAdmin)
admin.site.register(ReceivedEmailMessage, ReceivedEmailMessageAdmin)
