from django import forms


class EmailTemplateForm(forms.Form):
    message_template = forms.CharField(widget=forms.Textarea)
    subject = forms.CharField(max_length=255)
    file = forms.FileField(required=True,help_text="Select CSV file")
    only_gen = forms.BooleanField(required=False)


class SingleEmailForm(forms.Form):
    email = forms.EmailField()
    subject = forms.CharField(max_length=255)
    message = forms.CharField(widget=forms.Textarea)
