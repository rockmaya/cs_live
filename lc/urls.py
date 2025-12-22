from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.lc_create, name='lc_create'),
    path('', views.lc_list, name='lc_list'),  # placeholder for LC List page
    path('get_swift/', views.get_swift_code, name='lc_get_swift'),
    path("export/", views.lc_export, name="lc_export"),


    path("<int:pk>/edit/", views.lc_edit, name="lc_edit"),
    path("<int:pk>/delete/", views.lc_delete, name="lc_delete"),

    path('lc-autocomplete/', views.lc_number_autocomplete, name='lc_autocomplete'),

    # urls.py
    path('lc/<int:lc_id>/undo-close/', views.lc_undo_close, name='lc_undo_close'),




]
