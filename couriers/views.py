from django.shortcuts import get_object_or_404, render
import requests
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from couriers.models import Courier, MapField, WayBill
from django.db import transaction
from couriers.serializer import CourierGetSerializer, CourierSerializer, MapFieldSerializer, WayBillGetSerializer, WayBillSerializer
# Create your views here.


class ParentView(RetrieveAPIView, ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView):
    # custom Automator Class
    model = None
    serializer_class = None
    serializer_get_class = None
    permission_classes = [IsAuthenticated]
    exclude = []

    def dispatch(self, request, *args, **kwargs):
        if request.method in self.exclude:
            return Response("method not allowed", status=status.HTTP_403_FORBIDDEN)
        if request.method == 'GET' and self.serializer_get_class is not None:
            self.serializer_class = self.serializer_get_class
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, pk=None):
        if pk:
            self.kwargs['pk'] = pk
            return RetrieveAPIView.get(request)

        res = super().get(request, pk)
        return Response(res, status=status.HTTP_200_OK)

    def put(self, request, pk=None):
        self.kwargs['pk'] = pk
        return super().patch(request)


class CourierView(ParentView):
    model = Courier
    serializer_class = CourierSerializer
    serializer_get_class = CourierGetSerializer

    def prepare_courier_fields(self, courier, data=dict):
        # prepare map fields data before passing it to their serializer
        create_fields = data.get('create', None)
        cancel_fields = data.get('cancel', None)
        prepared_data = []
        if not create_fields or not cancel_fields:
            raise ValueError('create_fields is required')
        for key, index in create_fields.items():
            for field in index:
                prepared_data.append({
                    **field,
                    "courier_proccess_name": "create",
                    "courier_object_name": key,
                    "courier": courier.id
                })
        return prepared_data

    def post(self, request, *args, **kwargs):
        # post request body example
        """
        {
            courier:{
                'name':'ahmed',
                'email':'ahmed@gmail.com',
                'password':'ahmed_password',
                'token':'asd45as4d5as1d2as1d5a4sd54as21'
                'api_type':'1',
                'auth_type':'2'
                'domain':'https://ahmed-courier.com',
                'created_end_point':'/create_order',
                'retrive_end_point':'/retrive',
                'status_end_point':'/status',
                'cancel_end_point':'/cancel',
                'cancelable': True,
            },
            fields:{
                'create':{
                    'main':[
                        {
                            'local_name':'sender',
                            'courier_field_name':'sender_data',
                            'field_type':'object',
                        },
                        {
                            'local_name':'recipient',
                            'courier_field_name':'recipient_data',
                            'field_type':'object',
                        },
                        {
                            'local_name':'dimensions',
                            'courier_field_name':'dimensions',
                            'field_type':'object',
                        },
                        {
                            'local_name':'package_type',
                            'courier_field_name':'package_type',
                            'field_type':'object',
                        },
                        {
                            'local_name':'items',
                            'courier_field_name':'charges_items',
                            'field_type':'array',
                        },
                        {
                            'local_name':'boxes',
                            'courier_field_name':'boxes',
                            'field_type':'object',
                        },
                    ],
                    'sender_data':[
                        {
                            'local_name':'sender__address_type',
                            'courier_field_name':'adress_type',
                            'field_type':'string',
                        },
                        {
                            'local_name':'sender__name',
                            'courier_field_name':'name',
                            'field_type':'string',
                        },
                        {
                            'local_name':'sender__latitude',
                            'courier_field_name':'lat',
                            'field_type':'string',
                        },
                        {
                            'local_name':'sender__longtude',
                            'courier_field_name':'lon',
                            'field_type':'string',
                        },
                    ],
                    'recipient_data':[
                        {
                            'local_name':'recipient__address_type',
                            'courier_field_name':'adress_type',
                            'field_type':'string',
                        },
                        {
                            'local_name':'recipient__name',
                            'courier_field_name':'name',
                            'field_type':'string',
                        },
                        {
                            'local_name':'recipient__latitude',
                            'courier_field_name':'lat',
                            'field_type':'string',
                        },
                        {
                            'local_name':'recipient__longtude',
                            'courier_field_name':'lon',
                            'field_type':'string',
                        },
                    ],
                    'dimensions':[
                        {
                            'local_name':'box__width',
                            'courier_field_name':'width',
                            'field_type':'string',
                        },
                        {
                            'local_name':'box__height',
                            'courier_field_name':'height',
                            'field_type':'string',
                        },
                        {
                            'local_name':'box__whight',
                            'courier_field_name':'whight',
                            'field_type':'string',
                        },
                    ],
                    'package_type':[
                        {
                            'local_name':'service_type',
                            'courier_field_name':'courier_type',
                            'field_type':'string',
                            'from_request':True
                        },
                    ],
                    'charge_items':[
                        {
                            'local_name':'charge_type',
                            'courier_field_name':'charge_type',
                            'field_type':'string',
                            courier_values:'cod, service_custom',
                            'from_request':True

                        },
                        {
                            'local_name':'paied',
                            'courier_field_name':'paid',
                            'field_type':'string',
                        },
                        {
                            'local_name':'charge',
                            'courier_field_name':'charge',
                            'field_type':'string',
                        },
                        },
                        {
                            'local_name':'payer',
                            'courier_field_name':'payer',
                            'field_type':'string',
                            courier_values:'recipient, sender, client',
                            'from_request':True

                        },
                    ],
                    boxes:[
                        {
                            'local_name':'box__description',
                            'courier_field_name':'description',
                            'field_type':'string',
                        },
                        {
                            'local_name':'box__width',
                            'courier_field_name':'width',
                            'field_type':'string',
                        },
                        {
                            'local_name':'box__length',
                            'courier_field_name':'length',
                            'field_type':'string',
                        },
                        {
                            'local_name':'box__weight',
                            'courier_field_name':'weight',
                            'field_type':'string',
                        },
                        {
                            'local_name':'items',
                            'courier_field_name':'line_items',
                            'field_type':'array',
                        },
                    ],
                    line_items:[
                        {
                            'local_name':'item__name',
                            'courier_field_name':'name',
                            'field_type':'string',
                        },                        
                        {
                            'local_name':'item__ean13_code',
                            'courier_field_name':'ean13_code',
                            'field_type':'string',
                        },                        
                        {
                            'local_name':'item__origin_country',
                            'courier_field_name':'origin_country',
                            'field_type':'string',
                        },                        
                        {
                            'local_name':'item__price_per_unit',
                            'courier_field_name':'price_per_unit',
                            'field_type':'string',
                        },                        
                        {
                            'local_name':'item__quantity',
                            'courier_field_name':'quantity',
                            'field_type':'string',
                        },                        
                        {
                            'local_name':'item__tax_code',
                            'courier_field_name':'tax_code',
                            'field_type':'string',
                        },                        
                        {
                            'local_name':'item__desc',
                            'courier_field_name':'desc',
                            'field_type':'string',
                        },                        
                        {
                            'local_name':'item__weight',
                            'courier_field_name':'weight',
                            'field_type':'string',
                        },                        
                    ]
                }
            }
        }

        """
        courier_data = request.data.pop('courier')
        serializer = self.serializer_class(data=courier_data)
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            try:
                courier = serializer.save()
                prepared_data = self.prepare_courier_fields(
                    courier, request.data)
                fields_serializer = MapFieldSerializer(
                    data=prepared_data, many=True)
                fields_serializer.is_valid()
                fields_serializer.save()
            except Exception as e:
                transaction.rollback()
                return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

        return super().post(request, *args, **kwargs)


class WayBillView(ParentView):
    model = WayBill
    serializer_class = WayBillSerializer
    serializer_get_class = WayBillGetSerializer

    def prepare_data(self, order, courier):
        # prepare order data object before passing it to the request
        courier_fields = MapField.objects.filter(courier=courier)
        main_fields = courier_fields.filter(courier_object_name='main')
        data = {}
        for field in main_fields:
            if field.field_type == 'object':
                nested_fields = courier_fields.filter(
                    courier_object_name=field.courier_field_name)
                for nested_field in nested_fields:
                    if nested_field.from_request:
                        data[field.courier_field_name][nested_field.courier_field_name] = self.request.data.get(
                            nested_field.local_name)
                    elif nested_field.field_type == 'array':
                        new_nested = courier_fields.filter(
                            courier_object_name=nested_field.courier_field_name)
                        data[field.courier_field_name][nested_field.courier_field_name] = [
                            {f.courier_field_name: item[f.local_name.split('__')[1]] for f in new_nested} for item in order[nested_field.local_name]]
                    splitted = nested_field.local_name.split('__')
                    data[field.courier_field_name][nested_field.courier_field_name] = order[splitted[0]
                                                                                            ][splitted[1]] if len(splitted) > 1 else order[splitted[0]]
            elif field.field_type == 'array':
                nested_fields = courier_fields.filter(
                    courier_object_name=field.courier_field_name)
                obj = {}
                for nested_field in nested_fields:
                    splitted = nested_field.local_name.split('__')
                    obj[nested_field.courier_field_name] = order[splitted[0]]
                    data[field.courier_field_name] = [obj]
            elif field.from_request == True:
                data[field.courier_field_name] = self.request.data.get(
                    field.local_name)
            else:
                data[field.courier_field_name] = order[field.local_name]
        return data

    def post(self, request, *args, **kwargs):
        # order data should come from order model
        order = {
            "sender": {
                "address_type": "Work",
                "name": "sender_1",
                "latitude": 12.325561,
                'longitude': 1522.2255
            },
            "recipient": {
                "address_type": "Home",
                "name": "recipient_1",
                "latitude": 12.325561,
                'longitude': 1522.2255
            },
            "box": {
                "discription": 'box_1',
                "width": 50,
                "height": 50,
                "length": 100,
                "weight": 70,
            },
            "items": [
                {
                    "name": "item_1",
                    "ean13_code": "sa121asdas23s",
                    "origin_country": "Egypt",
                    "price_per_unit": 650.00,
                    "quantity": "2",
                    "tax_code": "asd555",
                    "desc": "item_1",
                    "weight": 25
                }
            ],
            "paied": True,
            "charge": 0
        }
        courier = get_object_or_404(Courier, pk=kwargs.get('courier', None))
        prepared_data = self.prepare_data(order, courier)
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {courier.token}"
        }
        create_request = requests.post(
            url=f"{courier.domain}{courier.create_end_point}", data=prepared_data, headers=headers)
        if create_request.status_code not in [200, 201, 202]:
            return Response(create_request.json(), status=create_request.status_code)
        way_bill_data = {
            "order": "order_1",
            "courier": courier.id,
            "status": "status_1",
        }
        serializer = self.serializer_class(data=way_bill_data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        way_bill = self.get_object()
        courier = way_bill.courier
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {courier.token}"
        }
        status_request = requests.get(
            url=f"{courier.domain}{courier.status_end_point}/{way_bill.courier_order_id}", headers=headers)
        if status_request.status_code != 200:
            return Response(status_request.json(), status_request.status_code)
        request.data.update({
            "status": status_request.json().get('status')
        })
        return super().put(request, pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.method == 'GET' and self.kwargs.get('pk', None):
            way_bill = self.get_object()
            courier = way_bill.courier
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": f"Bearer {courier.token}"
            }
            status_request = requests.get(
                url=f"{courier.domain}{courier.retrive_end_point}/{way_bill.courier_order_id}", headers=headers)
            if status_request.status_code != 200:
                return Response(status_request.json(), status_request.status_code)
            context["courier_order_label"] = status_request.json().get('label')
        return context


class WayBillCancelView(ParentView):
    model = WayBill
    serializer_class = WayBillSerializer
    exclude = ['GET', 'POST', 'PATCH', 'DELETE']

    def put(self, request, pk=None):
        way_bill = self.get_object()
        courier = way_bill.courier
        if not courier.cancelable:
            return Response('Operation not allowed', status_code=status.HTTP_403_FORBIDDEN)
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {courier.token}"
        }
        status_request = requests.get(
            url=f"{courier.domain}{courier.cancel_end_point}/{way_bill.courier_order_id}", headers=headers)
        if status_request.status_code != 200:
            return Response(status_request.json(), status_request.status_code)
        request.data.update({
            "status": "canceld"
        })
        return super().put(request, pk)
