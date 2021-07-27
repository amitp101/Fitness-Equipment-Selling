from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views as auth_views
from admin1 import views 
urlpatterns = [
	path('index', views.index, name="admin-home"),

    path('login', views.adminLogin, name="admin-login"),
    path('logout',views.adminLogout, name="admin-logout"),

	path('add_user', views.add_user),
	path('', views.dashboard,name="admin-dashboard"),
	path('category',views.category),
	path('sub_category',views.sub_category),
	path('product',views.product),
	path('order/',views.order, name='order'),
    path('order_show/<int:id>',views.order_show),
    path('order_delete/<int:id>',views.order_delete),
	path('payment',views.payment),
    path('payment_show/<int:id>',views.payment_show),
    path('account',views.account),
    path('account_show/<int:id>',views.account_show),
    path('contactus',views.contactus),
	path('review',views.review),
    path('review_show/<int:id>',views.review_show),
	path('visitor',views.visitor),
	path('cat_delete/<int:id>',views.cat_delete),
    path('edit/<int:id>',views.edit),
    path('cat_data_update/<int:id>',views.edit_data_update),
    path('sub_category_delete/<int:id>',views.sub_category_delete),
    path('sub_category_edit/<int:id>',views.sub_category_edit),
    path('product_delete/<int:id>',views.product_delete),
    path('product_edit/<int:id>',views.product_edit),
    path('product_show1/<int:id>',views.product_show1),
    path('add_user_delete/<int:id>',views.add_user_delete),
    path('user_show/<int:id>',views.user_show),
    path('user_edit/<int:id>',views.user_edit),
    path('user_active/<int:id>', views.user_active),
    path('user_deactive/<int:id>', views.user_deactive),
    path('contactus_delete/<int:id>',views.contactus_delete),
    path('reply/<int:id>',views.reply),
    path('discount', views.discount),
    path('discount_delete/<int:id>',views.discount_delete),
    path('discount_edit/<int:id>',views.discount_edit),
    path('discount_show1/<int:id>',views.discount_show1),
    path("password-reset/", auth_views.PasswordResetView.as_view(template_name='admin1/password_reset.html'),
         name="admin_password_reset"),
    path("password-reset/done/",
         auth_views.PasswordResetDoneView.as_view(template_name='admin1/password_reset_done.html'),
         name="admin_password_reset_done"),
    path("password-reset-confirm/<uidb64>/<token>/",
         auth_views.PasswordResetConfirmView.as_view(template_name='admin1/password_reset_confirm.html'),
         name="admin_password_reset_confirm"),
    path("password-reset-complete/",
         auth_views.PasswordResetCompleteView.as_view(template_name='admin1/password_reset_complete.html'),
         name="admin_password_reset_complete"),
    path('export_pdf/', views.export_pdf, name='export-to-pdf'),
    
    


  ]