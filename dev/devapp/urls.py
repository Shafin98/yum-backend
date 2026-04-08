from django.urls import path
from . import views
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # CMS
    path('login/', views.login_view, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('', views.dashboard, name='dashboard'),
    path('contact_inbox/', views.contact_inbox, name='contact_inbox'),
    path('mark-seen/<int:id>/', views.mark_seen, name='mark_seen'),
    path('delete-message/<int:id>/', views.delete_message, name='delete_message'),
    #Service
    path('add-service/', views.add_service, name='add_new_service'),
    path('service-list/', views.service_list, name='service'),
    path('service-details/<slug:slug>/', views.service_details, name='service_details'),
    path('edit-service/<slug:slug>/', views.edit_service, name='edit_service'),
    path('delete-service/<slug:slug>/', views.delete_service, name='delete_service'),
    #logo
    path('add-logo/', views.add_logo, name='add_new_logo'),
    path('logo-view/', views.view_logo, name='logo'),
    path('logo-details/<slug:slug>/', views.logo_details, name='logo_details'),
    path('edit-logo/<slug:slug>/', views.edit_logo, name='edit_logo'),
    path('delete-logo/<slug:slug>/', views.delete_logo, name='delete_logo'),
    #Testimonial
    path('add-testimonial/', views.add_testimonial, name='add_new_testimonial'),
    path('view-client-testimonials/', views.view_testimonial, name='testimonial'),
    path('testimonial-details/<slug:slug>/', views.testimonial_details, name='testimonial_details'),
    path('edit-testimonial/<slug:slug>/', views.edit_testimonial, name='edit_testimonial'),
    path('delete-testimonial/<slug:slug>/', views.delete_testimonial, name='delete_testimonial'),
    #Project
    path('add-project/', views.add_projects, name='add_new_project'),
    path('view-project/', views.view_projects, name='project'),
    path('project-details/<slug:slug>/', views.project_details, name='project_details'),
    path('edit-project/<slug:slug>/', views.edit_project, name='edit_project'),
    path('delete-project/<slug:slug>/', views.delete_project, name='delete_project'),
    #Social Media Accounts
    path('add-accounts/', views.add_acc, name='add_new_accounts'),
    path('view-accounts/', views.social_media_acc, name='accounts'),
    path('accounts-details/<str:platform>/', views.accounts_details, name='accounts_details'),
    path('edit-accounts/<str:platform>/', views.edit_accounts, name='edit_accounts'),
    # About
    path('about/edit/', views.edit_about_us, name='edit_about_us'),

    # Values
    path('values/', views.view_values, name='value_list'),
    path('values/add/', views.add_value, name='add_value'),
    path('values/edit/<int:pk>/', views.edit_value, name='edit_value'),
    path('values/delete/<int:pk>/', views.delete_value, name='delete_value'),

    # Team
    path('team/', views.view_team_members, name='team_list'),
    path('team/add/', views.add_team_member, name='add_team_member'),
    path('team/edit/<int:pk>/', views.edit_team_member, name='edit_team_member'),
    path('team/delete/<int:pk>/', views.delete_team_member, name='delete_team_member'),

    # API endpoints
    path('api/v1/contact/', ContactCreateAPI.as_view()),
    # admin API (Private)
    # path("api/v1/admin/login/", AdminLoginAPI.as_view()),
    # path("api/v1/admin/logout/", AdminLogoutAPI.as_view()),
    # path("api/v1/admin/me/", AdminMeAPI.as_view()),
    # portfolio APIs (public)
    path("api/v1/portfolio/logos/", ClientLogoListAPI.as_view()),
    path("api/v1/portfolio/social-media/", SocialMediaAccountListAPI.as_view()),

    path("api/v1/portfolio/testimonials/", TestimonialListAPI.as_view()),
    path("api/v1/portfolio/projects/", ProjectListAPI.as_view()),
    path("api/v1/portfolio/categories/",CategoryListAPI.as_view()),
    path('api/v1/portfolio/about/', AboutUsView.as_view()),
    path('api/v1/portfolio/values/', ValueListView.as_view()),
    path('api/v1/portfolio/team/', TeamMemberListView.as_view()),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)