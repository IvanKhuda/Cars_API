from django import forms

from cars_api.models import Car


class PostForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ('brand', 'model', 'year', 'country', 'price', 'mileage', 'fuel', 'transmission', 'engine',
                  'body_stile', 'exterior_color', 'interior_color', 'image_url', 'on_sale', 'status')
        labels = {
            'brand': 'Car brand',
            'model': 'Car model',
            'year': 'Car year',
            'country': 'Country',
            'price': 'Car price',
            'mileage': 'Car mileage',
            'fuel': 'Type of fuel',
            'transmission': 'Car transmission',
            'engine': 'Car engine',
            'body_stile': 'Car body stile',
            'exterior_color': 'Car exterior color',
            'interior_color': 'Car interior color',
            'on_sale': 'On sale?',
            'image_url': 'Url to car image',
            'status': 'Post status'
        }
        widgets = {
            'brand': forms.TextInput(attrs={'class': 'form-control border border-4',
                                            'placeholder': 'Enter Car brand'}),
            'model': forms.TextInput(attrs={'class': 'form-control border border-4',
                                            'placeholder': 'Enter Car model'}),
            'year': forms.TextInput(attrs={'class': 'form-control border border-4',
                                           'placeholder': 'Car year'}),
            'country': forms.TextInput(attrs={'class': 'form-control border border-4',
                                              'placeholder': 'Enter Country'}),
            'price': forms.TextInput(attrs={'class': 'form-control border border-4',
                                            'placeholder': 'Enter Car price (USD)'}),
            'mileage': forms.TextInput(attrs={'class': 'form-control border border-4',
                                              'placeholder': 'Enter Car mileage (km)'}),
            'fuel': forms.TextInput(attrs={'class': 'form-control border border-4',
                                           'placeholder': 'Enter Car fuel'}),
            'transmission': forms.TextInput(attrs={'class': 'form-control border border-4',
                                                   'placeholder': 'Enter Car transmission'}),
            'engine': forms.TextInput(attrs={'class': 'form-control border border-4',
                                             'placeholder': 'Enter Car engine'}),
            'body_stile': forms.TextInput(attrs={'class': 'form-control border border-4',
                                                 'placeholder': 'Enter Car body stile'}),
            'exterior_color': forms.TextInput(attrs={'class': 'form-control border border-4',
                                                     'placeholder': 'Enter Car exterior color'}),
            'interior_color': forms.TextInput(attrs={'class': 'form-control border border-4',
                                                     'placeholder': 'Enter Car interior color'}),
            'image_url': forms.URLInput(attrs={'class': 'form-control border border-4',
                                               'placeholder': 'Enter the image post URL'}),
            'status': forms.Select(attrs={'class': 'form-control border border-4'})
        }
