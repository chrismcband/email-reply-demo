from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView
from email import message_from_string
from email.utils import parseaddr
import dateutil.parser
from .models import EmailMessage, ReceivedEmailMessage, EmailHeader
from .forms import EmailMessageForm


class EmailCreateView(LoginRequiredMixin, CreateView):
    model = EmailMessage
    form_class = EmailMessageForm
    success_url = reverse_lazy('emails:list')


class EmailDetailView(LoginRequiredMixin, DetailView):
    model = EmailMessage
    # These next two lines tell the view to index lookups by id
    slug_field = 'id'
    slug_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        email_message = self.get_object()
        context['replies'] = ReceivedEmailMessage.objects.filter(
            headers__name='In-Reply-To',
            headers__value=email_message.message_id)

        return context


class EmailListView(LoginRequiredMixin, ListView):
    model = EmailMessage
    # These next two lines tell the view to index lookups by id
    slug_field = 'id'
    slug_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['form'] = EmailMessageForm()
        return context


def parse(self, request):
    data = request.body.decode('utf8')
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
        recipient_email=recipient_email,
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
                recipient_email.plain_content = decoded_content
            elif content_type == 'text/html':
                recipient_email.html_content = decoded_content

    received_email.save()

    for name, value in headers:
        received_email.headers.add(
            EmailHeader.objects.create(name=name, value=value))

    return HttpResponse(status=201)
