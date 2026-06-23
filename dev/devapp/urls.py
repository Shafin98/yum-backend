from django.urls import path
from . import views
from .views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    # ===========================================================================
    # CMS — AUTH
    # ===========================================================================
    path('login/', views.login_view, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('', views.dashboard, name='dashboard'),

    # ===========================================================================
    # CMS — INBOX
    # ===========================================================================
    path('contact_inbox/', views.contact_inbox, name='contact_inbox'),
    path('mark-seen/<int:id>/', views.mark_seen, name='mark_seen'),
    path('delete-message/<int:id>/', views.delete_message, name='delete_message'),

    # ===========================================================================
    # CMS — SERVICES  (Category → Service)
    # ===========================================================================
    path('add-service/', views.add_service, name='add_new_service'),
    path('service-list/', views.service_list, name='service'),
    path('service-details/<slug:slug>/', views.service_details, name='service_details'),
    path('edit-service/<slug:slug>/', views.edit_service, name='edit_service'),
    path('delete-service/<slug:slug>/', views.delete_service, name='delete_service'),

    # ── Service sub-resources (add: by service slug / delete: by record pk) ──
    # Badges
    path('service/<slug:slug>/badge/add/', views.add_service_badge, name='add_service_badge'),
    path('service/badge/<int:pk>/delete/', views.delete_service_badge, name='delete_service_badge'),
    # Process steps
    path('service/<slug:slug>/process/add/', views.add_service_process, name='add_service_process'),
    path('service/process/<int:pk>/delete/', views.delete_service_process, name='delete_service_process'),
    # Gallery
    path('service/<slug:slug>/gallery/add/', views.add_service_gallery, name='add_service_gallery'),
    path('service/gallery/<int:pk>/delete/', views.delete_service_gallery, name='delete_service_gallery'),
    # Deliverables
    path('service/<slug:slug>/deliverable/add/', views.add_service_deliverable, name='add_service_deliverable'),
    path('service/deliverable/<int:pk>/delete/', views.delete_service_deliverable, name='delete_service_deliverable'),
    # Tools
    path('service/<slug:slug>/tool/add/', views.add_service_tool, name='add_service_tool'),
    path('service/tool/<int:pk>/delete/', views.delete_service_tool, name='delete_service_tool'),
    # Pricing tiers
    path('service/<slug:slug>/pricing-tier/add/', views.add_service_pricing_tier, name='add_service_pricing_tier'),
    path('service/pricing-tier/<int:pk>/delete/', views.delete_service_pricing_tier, name='delete_service_pricing_tier'),
    # Pricing features (add is by tier pk, not service slug)
    path('service/pricing-tier/<int:pk>/feature/add/', views.add_service_pricing_feature, name='add_service_pricing_feature'),
    path('service/pricing-feature/<int:pk>/delete/', views.delete_service_pricing_feature, name='delete_service_pricing_feature'),
    # Reviews
    path('service/<slug:slug>/review/add/', views.add_service_review, name='add_service_review'),
    path('service/review/<int:pk>/delete/', views.delete_service_review, name='delete_service_review'),
    # Related services
    path('service/<slug:slug>/related/add/', views.add_service_related, name='add_service_related'),
    path('service/related/<int:pk>/delete/', views.delete_service_related, name='delete_service_related'),

    # ===========================================================================
    # CMS — LOGOS
    # ===========================================================================
    path('add-logo/', views.add_logo, name='add_new_logo'),
    path('logo-view/', views.view_logo, name='logo'),
    path('logo-details/<slug:slug>/', views.logo_details, name='logo_details'),
    path('edit-logo/<slug:slug>/', views.edit_logo, name='edit_logo'),
    path('delete-logo/<slug:slug>/', views.delete_logo, name='delete_logo'),

    # ===========================================================================
    # CMS — TESTIMONIALS  (slug → pk, since slug was removed from model)
    # ===========================================================================
    path('add-testimonial/', views.add_testimonial, name='add_new_testimonial'),
    path('view-client-testimonials/', views.view_testimonial, name='testimonial'),
    path('testimonial-details/<slug:slug>/', views.testimonial_details, name='testimonial_details'),
    path('edit-testimonial/<slug:slug>/', views.edit_testimonial, name='edit_testimonial'),
    path('delete-testimonial/<slug:slug>/', views.delete_testimonial, name='delete_testimonial'),

    # ===========================================================================
    # CMS — PROJECTS
    # ===========================================================================
    path('add-project/', views.add_projects, name='add_new_project'),
    path('view-project/', views.view_projects, name='project'),
    path('project-details/<slug:slug>/', views.project_details, name='project_details'),
    path('edit-project/<slug:slug>/', views.edit_project, name='edit_project'),
    path('delete-project/<slug:slug>/', views.delete_project, name='delete_project'),

    # ===========================================================================
    # CMS — SOCIAL MEDIA ACCOUNTS
    # ===========================================================================
    path('add-accounts/', views.add_acc, name='add_new_accounts'),
    path('view-accounts/', views.social_media_acc, name='accounts'),
    path('accounts-details/<str:platform>/', views.accounts_details, name='accounts_details'),
    path('edit-accounts/<str:platform>/', views.edit_accounts, name='edit_accounts'),

    # ===========================================================================
    # CMS — ABOUT US
    # ===========================================================================
    path('about/edit/', views.edit_about_us, name='edit_about_us'),

    # ===========================================================================
    # CMS — COMPANY VALUES
    # ===========================================================================
    path('values/', views.view_values, name='value_list'),
    path('values/add/', views.add_value, name='add_value'),
    path('values/edit/<int:pk>/', views.edit_value, name='edit_value'),
    path('values/delete/<int:pk>/', views.delete_value, name='delete_value'),

    # ===========================================================================
    # CMS — TEAM MEMBERS
    # ===========================================================================
    path('team/', views.view_team_members, name='team_list'),
    path('team/add/', views.add_team_member, name='add_team_member'),
    path('team/edit/<int:pk>/', views.edit_team_member, name='edit_team_member'),
    path('team/delete/<int:pk>/', views.delete_team_member, name='delete_team_member'),

    # ===========================================================================
    # API — CONTACT
    # ===========================================================================
    path('api/v1/contact/', ContactCreateAPI.as_view()),

    # ===========================================================================
    # API — PUBLIC PORTFOLIO
    # ===========================================================================
    path('api/v1/portfolio/logos/', ClientLogoListAPI.as_view()),
    path('api/v1/portfolio/social-media/', SocialMediaAccountListAPI.as_view()),
    path('api/v1/portfolio/testimonials/', TestimonialListAPI.as_view()),
    path('api/v1/portfolio/projects/', ProjectListAPI.as_view()),
    path('api/v1/portfolio/about/', AboutUsView.as_view()),
    path('api/v1/portfolio/values/', ValueListView.as_view()),
    path('api/v1/portfolio/team/', TeamMemberListView.as_view()),

    # Services — list & detail
    path('api/v1/portfolio/services/', ServiceListAPI.as_view()),
    path('api/v1/portfolio/services/<slug:slug>/', ServiceDetailAPI.as_view()),

    # Services — sub-resource endpoints
    path('api/v1/portfolio/services/<slug:slug>/process/', ServiceProcessAPI.as_view()),
    path('api/v1/portfolio/services/<slug:slug>/gallery/', ServiceGalleryAPI.as_view()),
    path('api/v1/portfolio/services/<slug:slug>/deliverables/', ServiceDeliverablesAPI.as_view()),
    path('api/v1/portfolio/services/<slug:slug>/tools/', ServiceToolsAPI.as_view()),
    path('api/v1/portfolio/services/<slug:slug>/pricingtiers/', ServicePricingTiersAPI.as_view()),
    path('api/v1/portfolio/services/<slug:slug>/reviews/', ServiceReviewsAPI.as_view()),
    path('api/v1/portfolio/services/<slug:slug>/related/', ServiceRelatedAPI.as_view()),
    # path('api/v1/portfolio/categories/', CategoryListAPI.as_view()),  # REMOVED — use /services/

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)