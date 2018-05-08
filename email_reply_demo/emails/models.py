from django.db import models


class EmailMessage(models.Model):
    sender_name = models.CharField(blank=True, max_length=300)
    sender_email_address = models.CharField(max_length=320)
    recipient_name = models.CharField(blank=True, max_length=300)
    recipient_email_address = models.CharField(max_length=320)
    reply_name = models.CharField(blank=True, max_length=300)
    reply_email_address = models.CharField(blank=True, max_length=320)
    subject = models.CharField(max_length=300)
    plain_content = models.TextField(blank=True)
    html_content = models.TextField(blank=True)
    event_description = models.CharField(blank=True, max_length=100)
    message_id = models.CharField(max_length=100, blank=True)
    created = models.DateTimeField(blank=True, auto_now_add=True)
    send_after = models.DateTimeField(blank=True, null=True)

    UNSENT = 0
    SENDING = 1
    FAILED_TO_QUEUE = 2
    SENT = 3
    TO_BE_REMOVED_FROM_THE_QUEUE = 4
    REMOVED_FROM_THE_QUEUE = 5
    FAILED_TO_SEND = 6

    SENDING_STATUSES = (
        (UNSENT, 'Unsent'),
        (SENDING, 'Sending'),
        (FAILED_TO_QUEUE, 'Failed to queue'),
        (SENT, 'Sent'),
        (TO_BE_REMOVED_FROM_THE_QUEUE, 'To be removed from the queue'),
        (REMOVED_FROM_THE_QUEUE, 'Removed from the queue'),
        (FAILED_TO_SEND, 'Failed to send')
    )

    sending_status = models.PositiveSmallIntegerField(default=UNSENT,
                                                      choices=SENDING_STATUSES)
    resend_count = models.PositiveSmallIntegerField(default=0)


class EmailHeader(models.Model):
    name = models.CharField(max_length=300)
    value = models.TextField()

    def __unicode__(self):
        return '%s: %s' % (self.name, self.value)


class ReceivedEmailMessage(models.Model):
    sender_name = models.CharField(blank=True, max_length=300)
    sender_email_address = models.CharField(max_length=320)
    recipient_name = models.CharField(blank=True, max_length=300)
    recipient_email_address = models.CharField(max_length=320)
    date = models.DateTimeField()
    subject = models.TextField(blank=True)
    headers = models.ManyToManyField(EmailHeader)
    plain_content = models.TextField()
    html_content = models.TextField()
