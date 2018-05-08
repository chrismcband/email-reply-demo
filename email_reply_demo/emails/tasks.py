from celery import shared_task
from celery.utils.log import get_task_logger
from django.conf import settings
from mailshake import EmailMessage as EmailMessageContainer, AmazonSESMailer, \
    ToConsoleMailer
from email_reply_demo.emails.models import EmailMessage
from email_reply_demo.taskapp.celery import app as celery_app


@shared_task(bind=True)
def send_email_task(self, email_id):
    logger = get_task_logger(__name__)
    try:
        email_message = EmailMessage.objects.get(id=email_id)
    except EmailMessage.DoesNotExist:
        return False

    email_message.sending_status = EmailMessage.SENDING
    email_message.save()

    from_email = email_message.sender_email_address

    if email_message.sender_name.strip() != '':
        from_email = '%s <%s>' % (email_message.sender_name,
                                  email_message.sender_email_address)

    to_email = email_message.recipient_email_address
    if email_message.recipient_name.strip() != '':
        to_email = '%s <%s>' % (email_message.recipient_name,
                                email_message.recipient_email_address)

    reply_email = []

    if email_message.reply_email_address.strip() != '':
        reply_email = [email_message.reply_email_address]
        if email_message.reply_name.strip() != '':
            reply_email = '%s <%s>' % (email_message.reply_name,
                                       email_message.reply_email_address)
            reply_email = [reply_email]

    message_package = EmailMessageContainer(
        subject=email_message.subject,
        text_content=email_message.plain_content,
        html_content=email_message.html_content,
        from_email=from_email,
        to=to_email,
        reply_to=reply_email
    )

    # Send to the console
    mailer = ToConsoleMailer()
    mailer.send_messages(message_package)

    mailer = AmazonSESMailer(
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name='eu-west-1'
    )
    responses = mailer.send_messages(message_package)

    if len(responses) < 1:
        email_message.sending_status = email_message.FAILED_TO_SEND
        email_message.save()
        logger.error("Unable to send email #%s" % email_message.pk)
        return False

    email_message.sending_status = EmailMessage.SENT
    email_message.message_id = responses[0].get('MessageId')
    email_message.save()
    logger.info("Sent email %s" % email_message)
    return True