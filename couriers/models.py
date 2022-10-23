from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Courier(models.Model):
    json, soap = "1", "2"
    email_password, token = '1', '2'
    TYPE = {
        (json, "JSON"),
        (soap, "SOAP"),
    }

    AUTH = {
        (email_password, 'EMAIL_PASSWORD'),
        (token, 'TOKEN'),
    }

    name = models.CharField(_("Name"), max_length=255)
    email = models.EmailField(_("Email"), max_length=255)
    password = models.CharField(_("Password"), max_length=255),
    api_type = models.CharField(_("Api Type"), max_length=5, choices=TYPE)
    auth_type = models.CharField(_("Auth Type"), max_length=20, choices=AUTH)
    domain = models.URLField(_("Domain"), max_length=200)

    create_end_point = models.CharField(_("Create End point"), max_length=200)
    retrive_end_point = models.CharField(
        _("Retrive End point"), max_length=200)
    status_end_point = models.CharField(_("Status End point"), max_length=200)
    cancel_end_point = models.CharField(
        _("Cancel End point"), max_length=200, null=True, blank=True)
    countries_end_point = models.CharField(
        _("Countries End point"), max_length=200, null=True, blank=True)
    cities_end_point = models.CharField(
        _("Countries End point"), max_length=200, null=True, blank=True)
    service_types_end_point = models.CharField(
        _("Service Types End point"), max_length=200, null=True, blank=True)

    cancelable = models.BooleanField(_("Can Cancel"), default=False)

    def __str__(self):
        return self.name


class MapField(models.Model):

    local_name = models.CharField(_("Local Name"), max_length=255)
    courier_field_name = models.CharField(
        _("Courier Field Name"), max_length=255)
    courier_object_name = models.CharField(
        _("Courier Model Name"), max_length=255)
    courier_proccess = models.CharField(_("Courier Proccess"), max_length=50)
    field_type = models.CharField(_("Field Type"), max_length=50)
    courier = models.ForeignKey(
        'couriers.Courier', related_name='map_fields', on_delete=models.CASCADE)
    courier_values = models.TextField(
        _("Courier Values"), null=True, blank=True)
    from_request = models.BooleanField(_("From Request"), default=False)

    class Meta:
        verbose_name = _("MapField")
        verbose_name_plural = _("MapFields")

    def __str__(self):
        return f"{self.local_name} --> {self.courier_field_name} ({self.courier.name})"


class WayBill(models.Model):
    # must be a foreign key from Orders Table
    order = models.CharField(_("order"), max_length=50)
    courier = models.ForeignKey("couriers.Courier", verbose_name=_(
        "Courier"), on_delete=models.CASCADE)
    status = models.CharField(_("Status"), max_length=50)
    courier_order_id = models.CharField(_("Courier Order ID"), max_length=100)

    class Meta:
        verbose_name = _("Way Bill")
        verbose_name_plural = _("Way Bills")

    def __str__(self):
        return self.name
