from django.contrib import admin

from cars_api.models import Car


@admin.register(Car)
class PostAdmin(admin.ModelAdmin):
    list_display = ('brand', 'model', 'year', 'country', 'body_stile', 'price', 'mileage', 'exterior_color',
                    'interior_color', 'fuel', 'transmission', 'engine', 'on_sale', 'owner', 'slug', 'status', 'publish')
    list_filter = ('status', 'created', 'publish', 'brand', 'model', 'year', 'country', 'price', 'mileage', 'fuel',
                   'transmission', 'engine', 'body_stile', 'exterior_color', 'interior_color', 'on_sale', 'owner')
    search_fields = ('brand', 'model')
    prepopulated_fields = {'slug': ('brand', 'model', 'year')}
    raw_id_fields = ('owner',)
    ordering = ('-status', '-publish')
