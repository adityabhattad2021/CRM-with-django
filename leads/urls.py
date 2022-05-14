from django.urls import path
from .views import LeadCreateView,LeadListView,LeadDetailView,LeadUpdateView,LeadDeleteView,AssignAgentView,CategoryListView,CategoryDetailView,LeadCategoryUpdateView

app_name="leads"

urlpatterns = [
    path('',LeadListView.as_view(),name='leads-page'),
    path('create/',LeadCreateView.as_view(),name='create-page'),
    path('<int:pk>/',LeadDetailView.as_view(),name='lead-page'),
    path('<int:pk>/update/',LeadUpdateView.as_view(),name='update-page'),
    path('<int:pk>/delete/',LeadDeleteView.as_view(),name='delete'),
    path('<int:pk>/assign-agent',AssignAgentView.as_view(),name='assign-agent'),
    path('category-list/',CategoryListView.as_view(),name='catogery-page'),
    path('category-detail/<int:pk>',CategoryDetailView.as_view(),name='category-detail'),
    path('<int:pk>/category-update/',LeadCategoryUpdateView.as_view(),name='category-update')
]
