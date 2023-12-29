from django import forms


class BroadcasForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea, label = "Сообщение для рассылки")
