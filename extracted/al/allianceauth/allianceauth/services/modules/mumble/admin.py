from django.contrib import admin
from django import forms

from .models import IdlerHandler, MumbleServerServer, MumbleUser
from ...admin import ServicesUserAdmin

@admin.register(MumbleUser)
class MumbleUserAdmin(ServicesUserAdmin):
    list_display = ServicesUserAdmin.list_display + (
        'username',
        'release',
        'version'
    )
    search_fields = ServicesUserAdmin.search_fields + (
        'username',
    )


@admin.register(MumbleServerServer)
class MumbleServerServerAdmin(admin.ModelAdmin):
    list_display = ["name", "ip", "port", "slice", "virtual_servers", "avatar_enable", "reject_on_error", "offset"]
    list_filter = ["slice", "avatar_enable", "reject_on_error", "offset"]
    search_fields = ["name"]


class IdlerHandlerForm(forms.ModelForm):
    class Meta:
        model = IdlerHandler
        fields = '__all__'

    def clean_list(self):
        channel_list = self.cleaned_data['list']
        channel_ids = [x for x in channel_list.split(',') if x]
        output = []
        for x in channel_ids:
            x = x.strip()
            try:
                int(x)
            except ValueError:
                raise forms.ValidationError(f"Unrecognized channel ID '{x}'")
            else:
                output.append(x)
        return ','.join(output)


@admin.register(IdlerHandler)
class IdlerhandlerAdmin(admin.ModelAdmin):
    list_display = ["name", "enabled", "seconds", "interval", "channel", "denylist"]
    list_filter = ["enabled", "denylist"]
    search_fields = ["name"]
    form = IdlerHandlerForm
