from .models import Ikili

from django.forms import ModelForm


class IkiliForm(ModelForm):
    class Meta:
        model = Ikili
        fields = ['tweet_id']
