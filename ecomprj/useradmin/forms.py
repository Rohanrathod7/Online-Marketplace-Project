from core.models import Product
from django import forms 

INPUT_CLASSES='form-control pt-3 pb-3 ps-4 mb-2' 
INPUT_STYLE = 'color: black'
DESC_INPUT_STYLE = 'color: black;height: 100px;'

class AddProduct(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Enter Product Title", "class":INPUT_CLASSES, 'style':INPUT_STYLE}))
    description = forms.CharField(widget=forms.Textarea(attrs={"placeholder":"Enter Product Description", "class":INPUT_CLASSES, 'style':DESC_INPUT_STYLE}))
    price = forms.DecimalField(widget=forms.NumberInput(attrs={"placeholder":"Enter Product Price", "class":INPUT_CLASSES, 'style':INPUT_STYLE}))
    old_price = forms.DecimalField(widget=forms.NumberInput(attrs={"placeholder":"Enter Old Price", "class":INPUT_CLASSES, 'style':INPUT_STYLE}))
    type = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Enter Product Type", "class":INPUT_CLASSES, 'style':INPUT_STYLE}))
    stock = forms.CharField(widget=forms.NumberInput(attrs={"placeholder":"Enter Product Title", "class":INPUT_CLASSES, 'style':INPUT_STYLE}))
    life = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Enter Product Life", "class":INPUT_CLASSES, 'style':INPUT_STYLE}))
    mfg = forms.DateField(widget=forms.DateInput(attrs={"placeholder":"Enter Manufacturing Date", "class":INPUT_CLASSES, 'style':INPUT_STYLE, 'type':'date'}))
    tags = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Enter Product Tags", "class":INPUT_CLASSES, 'style':INPUT_STYLE}))
    image = forms.ImageField(widget=forms.FileInput(attrs={ "class":"form-control"}))


    class Meta:
        model = Product
        fields = [
            'title',
            'image',
            'price',
            'description',
            'old_price',
            'stock',
            'type',
            'life',
            'mfg',
            'tags',
            
            'category',
            
        ]
