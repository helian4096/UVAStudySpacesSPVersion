from django.urls import path

from . import views


app_name = "study_spaces"
urlpatterns = [
    path("", views.home, name="homepage"),
    path("logout", views.logout_view, name="logout"),
    path("logout/", views.logout_view, name="logout"),
    path('login', views.login_view, name="login"),
    path('admin', views.admin_view, name="admin"),
    path('directions', views.directions, name="directions"),
    path('profile', views.profile, name='profile'),
    path('submission', views.submission, name='submission'),
    path('approve', views.approve_submission, name='approve'),
    path('deny', views.deny_submission, name='deny'),
    path('information', views.information, name='information'),
    path('closest', views.closest, name='closest'),
    path('edit/<int:study_space_id>/', views.edit_study_space, name='edit'),
    path('delete/<int:study_space_id>/', views.delete_study_space, name='delete'),
]
