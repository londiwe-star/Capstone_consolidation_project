"""
Admin interface configuration for the news application.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Publisher, Article, Newsletter


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Admin interface for CustomUser model."""
    list_display = ['username', 'email', 'role', 'first_name', 'last_name', 'is_staff']
    list_filter = ['role', 'is_staff', 'is_active']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Role & Profile', {
            'fields': ('role', 'bio', 'profile_picture')
        }),
        ('Reader Subscriptions', {
            'fields': ('subscribed_publishers', 'subscribed_journalists'),
            'classes': ('collapse',)
        }),
        ('Journalist Affiliations', {
            'fields': ('affiliated_publishers',),
            'classes': ('collapse',)
        }),
    )
    
    filter_horizontal = ['subscribed_publishers', 'subscribed_journalists', 'affiliated_publishers']


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    """Admin interface for Publisher model."""
    list_display = ['name', 'website', 'created_at']
    search_fields = ['name', 'description']
    list_filter = ['created_at']


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    """Admin interface for Article model."""
    list_display = ['title', 'author', 'publisher', 'is_approved', 'approved_by', 'created_at']
    list_filter = ['is_approved', 'created_at', 'publisher']
    search_fields = ['title', 'content', 'author__username']
    readonly_fields = ['approved_by', 'approved_at', 'created_at', 'updated_at']
    
    fieldsets = [
        ('Article Information', {
            'fields': ('title', 'summary', 'content', 'featured_image')
        }),
        ('Author & Publisher', {
            'fields': ('author', 'publisher')
        }),
        ('Approval Status', {
            'fields': ('is_approved', 'approved_by', 'approved_at')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'published_at'),
            'classes': ('collapse',)
        }),
    ]


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    """Admin interface for Newsletter model."""
    list_display = ['title', 'author', 'publisher', 'is_sent', 'sent_at', 'created_at']
    list_filter = ['is_sent', 'created_at', 'publisher']
    search_fields = ['title', 'content', 'author__username']
    readonly_fields = ['sent_at', 'created_at', 'updated_at']
