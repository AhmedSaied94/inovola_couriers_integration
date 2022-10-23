from django.urls import path

from couriers.views import CourierView, WayBillCancelView, WayBillView


urlpatterns = [
    path('WayBill/', WayBillView.as_view()),  # get list / post
    path('WayBill/<str:pk>', WayBillView.as_view()),  # get one / put

    path('WayBillCancel/<str:pk>', WayBillCancelView.as_view()),  # only put

    path('Courier/', CourierView.as_view()),  # get list / post
    path('Courier/<str:pk>', CourierView.as_view()),  # get one / put

]
