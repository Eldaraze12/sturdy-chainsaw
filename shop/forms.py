from django import forms

from .models import ContactMessage


class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "phone", "subject", "message"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "placeholder": "Adınız",
                    "class": "field-input",
                    "autocomplete": "name",
                }
            ),
            "phone": forms.TextInput(
                attrs={
                    "placeholder": "Telefon nömrəniz",
                    "class": "field-input",
                    "autocomplete": "tel",
                }
            ),
            "subject": forms.HiddenInput(),
            "message": forms.Textarea(
                attrs={
                    "placeholder": "Sifarişinizi buraya yazın...",
                    "class": "field-input",
                    "rows": 5,
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["subject"].initial = "Onlayn chat sifarişi"
        self.fields["name"].required = True
        self.fields["phone"].required = True

    def clean_message(self):
        message = self.cleaned_data["message"].strip()
        if not message:
            raise forms.ValidationError("Mesaj boş ola bilməz.")
        return message

    def clean_phone(self):
        phone = self.cleaned_data["phone"].strip()
        digits = [c for c in phone if c.isdigit()]
        if len(digits) < 7:
            raise forms.ValidationError("Zəhmət olmasa düzgün telefon nömrəsi daxil edin.")
        return phone
