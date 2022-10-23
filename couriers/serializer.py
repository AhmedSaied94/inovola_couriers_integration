import requests
from rest_framework import serializers
from couriers.models import Courier, MapField, WayBill


class MapFieldSerializer(serializers.ModelSerializer):

    class Meta:
        model = MapField
        fields = '__all__'


class CourierSerializer(serializers.ModelSerializer):

    class Meta:
        model = Courier
        fields = '__all__'


class CourierGetSerializer(serializers.ModelSerializer):

    courier_options = serializers.SerializerMethodField()
    map_fields = MapFieldSerializer(many=True)

    class Meta:
        model = Courier
        fields = '__all__'

    def get_courier_options(self, obj):
        # this field used to retrive courier custom data from courier web site to let the entry choose from them when create way bill
        options = {}
        fields = MapField.objects.filter(
            courier=obj, courier_values__isnull=False)
        for field in fields:
            options[field.local_name] = field.courier_values.split(',')
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {obj.token}'
        }
        if obj.cities_end_point:
            options['cities'] = requests.get(
                f'{obj.domain}{obj.cities_end_point}', headers=headers).json()
        if obj.countries_end_point:
            options['countries'] = requests.get(
                f'{obj.domain}{obj.countries_end_point}', headers=headers).json()
        if obj.servies_types_end_point:
            options['servies_types'] = requests.get(
                f'{obj.domain}{obj.servies_types_end_point}', headers=headers).json()


class WayBillSerializer(serializers.ModelSerializer):

    class Meta:
        model = WayBill
        fields = '__all__'


class WayBillGetSerializer(serializers.ModelSerializer):

    courier = CourierGetSerializer()
    courier_order_label = serializers.SerializerMethodField()

    class Meta:
        model = WayBill
        fields = '__all__'

    def get_courier_order_label(self, obj):
        return self.context.get('courier_order_label', None)
