from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from contacts.views import AdminContactView
from django.contrib.auth import views as auth_views

# Error handlers
handler400 = 'core.views.bad_request'
handler403 = 'core.views.permission_denied'
handler404 = 'core.views.page_not_found'
handler500 = 'core.views.server_error'

urlpatterns = i18n_patterns(
    # Language selection URLs
    path('i18n/', include('django_translation_flags.urls')),
    
    # Admin interface
    path('admin/', admin.site.urls),
    # Admin contact view
    path('admin/contact/', AdminContactView.as_view(), name='admin-contact'),
    
    # Core app URLs (main site)
    path('', include('core.urls')),  # This is the homepage under language prefix
    
    # Authentication URLs
    path('auth/', include('django.contrib.auth.urls')),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/auth/password_reset_done.html'
    ), name='password-reset-done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name="accounts/auth/password_reset_confirm.html"
    ), name='password-reset-confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/auth/password_reset_complete.html'
    ), name='password_reset_complete'),
    
    # Listings and documents
    path('listings/', include('listings.urls')),
    path('accounts/', include('accounts.urls')),
    path('contacts/', include('contacts.urls')),
    path('listings/', include('documents.urls')),
)

# Serve static and media files in DEBUG mode
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)