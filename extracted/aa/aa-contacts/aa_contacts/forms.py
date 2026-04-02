from django import forms

from .models import AllianceContact, CorporationContact


class AllianceContactForm(forms.ModelForm):
    class Meta:
        model = AllianceContact
        fields = ('contact_type', 'standing', 'labels', 'notes', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field, data in self.fields.items():
            if field != 'notes':
                data.disabled = True


class CorporationContactForm(forms.ModelForm):
    class Meta:
        model = CorporationContact
        fields = ('contact_type', 'standing', 'labels', 'notes', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field, data in self.fields.items():
            if field != 'notes':
                data.disabled = True
