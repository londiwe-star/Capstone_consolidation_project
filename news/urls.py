"""
URL configuration for the news app views.
"""
from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Articles
    path('articles/', views.article_list_view, name='article_list'),
    path('articles/<int:pk>/', views.article_detail_view, name='article_detail'),
    path('articles/create/', views.article_create_view, name='article_create'),
    path('articles/<int:pk>/edit/', views.article_update_view, name='article_update'),
    path('articles/<int:pk>/delete/', views.article_delete_view, name='article_delete'),
    path('articles/<int:pk>/approve/', views.article_approve_view, name='article_approve'),
    
    # Dashboards
    path('dashboard/journalist/', views.journalist_dashboard_view, name='journalist_dashboard'),
    path('dashboard/editor/', views.editor_dashboard_view, name='editor_dashboard'),
    path('dashboard/reader/', views.reader_dashboard_view, name='reader_dashboard'),
    
    # Publishers
    path('publishers/', views.publisher_list_view, name='publisher_list'),
    path('publishers/create/', views.publisher_create_view, name='publisher_create'),
    path('publishers/<int:pk>/', views.publisher_detail_view, name='publisher_detail'),
    path('publishers/<int:pk>/subscribe/', views.toggle_publisher_subscription, name='toggle_publisher_subscription'),
    
    # Journalists
    path('journalists/<int:pk>/', views.journalist_profile_view, name='journalist_profile'),
    path('journalists/<int:pk>/subscribe/', views.toggle_journalist_subscription, name='toggle_journalist_subscription'),
]
