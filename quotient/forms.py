from django import forms

class MappingClassForm(forms.Form):
    genus = forms.IntegerField()
    punctures = forms.IntegerField()
    words = forms.CharField(max_length=1000, required=False)
    
    def clean(self):
        cleaned_data = super(MappingClassForm, self).clean()
        genus = cleaned_data.get('genus')
        punctures = cleaned_data.get('punctures')
        words = cleaned_data.get('words')
        if genus < 0:
            raise forms.ValidationError('Genus must be a non-negative integer')
        if punctures < 1:
            raise forms.ValidationError('Punctures must be a positive integer')
