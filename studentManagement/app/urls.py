from django.contrib import admin
from django.urls import path,include

from app import views

urlpatterns = [

    path('',views.index,name='index'),
    path('login_page/',views.login_page,name='login_page'),
    path('HOD/',views.HOD,name='HOD'),
    path('STAFF/',views.STAFF,name='STAFF'),
    path('dash/',views.dash,name='dash'),
    path('profile/',views.profile,name='profile'),
    path('profile_update/',views.profile_update,name='profile_update'),
    path('add_staff/',views.add_staff,name='add_staff'),
    path('logout_page/', views.logout_page, name='logout_page'),
    path('views_staff/', views.views_staff, name='views_staff'),
    path('edit_staff/<str:id>', views.edit_staff, name='edit_staff'),
    path('update_staff/', views.update_staff, name='update_staff'),
    path('delete_staff/<int:admin>/', views.delete_staff, name='delete_staff'),
    path('add_course/', views.add_course, name='add_course'),
    path('view_course/', views.view_course, name='view_course'),
    path('edit_course/<int:id>/', views.edit_course, name='edit_course'),
    path('delete_course/<int:id>/', views.delete_course, name='delete_course'),
    path('update_course/', views.update_course, name='update_course'),
    path('add_subject/', views.add_subject, name='add_subject'),
    path('view_subject/', views.view_subject, name='view_subject'),
    path('edit_subject/<str:id>', views.edit_subject, name='edit_subject'),
    path('update_subject/',views.update_subject, name='update_subject'),
    path('delete_subject/<str:id>',views.delete_subject, name='delete_subject'),
    path('add_session/', views.add_session, name='add_session'),
    path('view_session/',views.view_session, name='view_session'),
    path('edit_session/<str:id>', views.edit_session, name='edit_session'),
    path('update_session/',views.update_session, name='update_session'),
    path('delete_session/<str:id>',views.delete_session, name='delete_session'),
    path('send_staff_notifications/', views.send_staff_notifications, name='send_staff_notifications'),
    path('save_staff_notifications',views.save_staff_notifications, name='save_staff_notifications'),
    path('notify_view', views.notify_view, name='notify_view'),
    path('notifications_done/<str:status>',views.notifications_done, name='notifications_done'),
    path('staff_feedback', views.staff_feedback, name='staff_feedback'),
    path('save_feedback',views.save_feedback, name='save_feedback'),
    path('staff_feedback_view', views.staff_feedback_view, name='staff_feedback_view'),
    path('staff_feedback_view', views.staff_feedback_view, name='staff_feedback_view'),
    path('apply_leave',views.apply_leave, name='apply_leave'),
    path('staff_leave_view',views.staff_leave_view,name='staff_leave_view'),
    path('staff_approve_leave/<str:id>',views.staff_approve_leave,name='staff_approve_leave'),
    path('staff_disapprove_leave/<str:id>',views.staff_disapprove_leave,name='staff_disapprove_leave'),
]

