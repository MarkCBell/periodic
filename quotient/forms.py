from django import forms

class MappingClassForm(forms.Form):
    genus = forms.CharField(max_length=10)
    punctures = forms.CharField(max_length=10)
    word = forms.CharField(max_length=1000)
    
    def clean(self):
        cleaned_data = super(MappingClassForm, self).clean()
        genus = cleaned_data.get('genus')
        punctures = cleaned_data.get('punctures')
        word = cleaned_data.get('word')
        if not genus.isnumeric() or int(genus) < 0:
            raise forms.ValidationError('Genus must be a non-negative integer')
        if not punctures.isnumeric() or int(punctures) < 1:
            raise forms.ValidationError('Punctures must be a positive integer')
