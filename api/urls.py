from django.urls import path, include
from .views import get_create_projects, get_delete_project_by_id, get_add_domains_in_project
from .views import get_delete_domain_in_project_by_id, get_add_vulns_in_domain_by_id, get_update_vulns_by_id

urlpatterns = [
    path('projects', get_create_projects, name = "get_post_projects"),
    path('projects/<int:pk>', get_delete_project_by_id, name = "get_delete_project_by_id"),
    path('projects/<int:pk>/domains', get_add_domains_in_project, name = "get_add_domains_in_project"),
    path('projects/<int:pk>/domains/<int:dk>', get_delete_domain_in_project_by_id, name = "delete_domain_in_project_by_id"),
    path('projects/<int:pk>/domains/<int:dk>/vulns', get_add_vulns_in_domain_by_id, name = "delete_domain_in_project_by_id"),
    path('projects/<int:pk>/domains/<int:dk>/vulns/<int:vk>', get_update_vulns_by_id, name = "get_update_vulns_by_id"),
]
