from django import forms

class FormComentario(forms.Form):

	content_type = forms.CharField(widget=forms.HiddenInput)
	object_id = forms.IntegerField(widget=forms.HiddenInput)
	respuesta = forms.CharField(label='', widget=forms.Textarea)