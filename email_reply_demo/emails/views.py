from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.db.transaction import on_commit
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, DetailView, ListView
from email import message_from_string
from email.utils import parseaddr
import re
import dateutil.parser
from .models import EmailMessage, ReceivedEmailMessage, EmailHeader
from .forms import EmailMessageForm
from .tasks import send_email_task


class EmailCreateView(LoginRequiredMixin, CreateView):
    model = EmailMessage
    form_class = EmailMessageForm
    success_url = reverse_lazy('emails:list')

    def form_valid(self, form):
        self.object = form.save()
        self.object.sender_name = 'Notifications'
        self.object.sender_email_address = \
            'alerts@notifications.chrismcdonald.ltd'
        self.object.html_content = ''
        self.object.save()

        on_commit(lambda: send_email_task.delay(self.object.id))

        return HttpResponseRedirect(self.get_success_url())


class EmailDetailView(LoginRequiredMixin, DetailView):
    model = EmailMessage
    # These next two lines tell the view to index lookups by id
    slug_field = 'id'
    slug_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        email_message = self.get_object()

        return context


class EmailListView(LoginRequiredMixin, ListView):
    model = EmailMessage
    # These next two lines tell the view to index lookups by id
    slug_field = 'id'
    slug_url_kwarg = 'id'

    def get_queryset(self):
        queryset = super(EmailListView, self).get_queryset()

        return queryset.annotate(reply_count=Count('receivedemailmessage'))

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['form'] = EmailMessageForm()
        return context


@csrf_exempt
def parse(request):
    print(request.body)
    data = request.body.decode('utf8')
    print(data)
    email_message = message_from_string(data)

    # get all headers
    headers = email_message.items()

    # get a single header
    subject = email_message.get('Subject')
    from_address = email_message.get('From')
    sender_name, sender_email = parseaddr(from_address)
    date = dateutil.parser.parse(
        email_message.get('Date'))
    to_address = email_message.get('To')
    recipient_name, recipient_email = parseaddr(to_address)

    received_email = ReceivedEmailMessage(
        sender_name=sender_name,
        sender_email_address=sender_email,
        recipient_name=recipient_name,
        recipient_email_address=recipient_email,
        date=date,
        subject=subject)

    if email_message.is_multipart():
        messages = email_message.get_payload()
        for sub_message in messages:
            content = sub_message.get_payload(decode=True)
            decoded_content = content.decode(
                encoding=sub_message.get_content_charset())

            # content type could be 'text/plain',
            # 'text/html' or any MIME type (attachments)
            content_type = sub_message.get_content_type()

            if content_type == 'text/plain':
                received_email.plain_content = decoded_content
            elif content_type == 'text/html':
                received_email.html_content = decoded_content

    received_email.save()

    for name, value in headers:
        received_email.headers.add(
            EmailHeader.objects.create(name=name, value=value))
        if name == 'In-Reply-To':
            p = re.compile('<(.*)@eu-west-1.amazonses.com>')
            match = p.match(value)

            if match:
                message_id = match.group(1)

                try:
                    email_message = EmailMessage.objects.get(
                        message_id=message_id)
                    received_email.reply_to_email = email_message
                except EmailMessage.DoesNotExit:
                    print('Unable to find matching message id')
                    return HttpResponse(status=403)

    received_email.save()

    return HttpResponse(status=201)
