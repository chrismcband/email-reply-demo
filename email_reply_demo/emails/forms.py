from django.forms import ModelForm, CharField, EmailField, Textarea
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import EmailMessage


class EmailMessageForm(ModelForm):
    recipient_name = CharField(
        label='Recipient name',
        required=True)
    recipient_email_address = EmailField(
        label='Recipient email',
        required=True)
    plain_content = CharField(
        label='Message',
        required=True,
        widget=Textarea)

    def __init__(self, *args, **kwargs):
        super(EmailMessageForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Send'))

    class Meta:
        model = EmailMessage
        fields = ['subject', 'recipient_name', 'recipient_email_address',
                  'plain_content']
