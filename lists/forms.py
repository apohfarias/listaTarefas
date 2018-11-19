from django import forms
from lists.models import Item
from django.core.exceptions import ValidationError

EMPTY_ITEM_ERROR = "Itens da lista nao podem estar em branco!!!"
DUPLICATE_ITEM_ERROR = "Você já tem esse item na lista!"

class ItemForm(forms.models.ModelForm):
	class Meta:
		model = Item
		fields = ('text',)
		widgets = {
			'text': forms.fields.TextInput(attrs={
				'placeholder': 'Enter a to-do item',
				'class': 'form-control input-lg',
			}),			
		}

		error_messages = {
			'text': {'required': EMPTY_ITEM_ERROR}
		}

	def save(self, for_list):
		self.instance.list = for_list
		return super().save()


class ExistingListItemForm(ItemForm):

	def __init__(self, for_list, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.instance.list = for_list


	def validate_unique(self):
		try:
			self.instance.validate_unique()
		except ValidationError as e:
			e.error_dict = {'text': [DUPLICATE_ITEM_ERROR]}
			self._update_errors(e)

	def save(self):
		return forms.models.ModelForm.save(self)