from django.urls import path
from .views import AgentListView,AgentCreateView,AgentDetailView,AgentUpdateView,AgentDeleteView

app_name="agents"

urlpatterns = [
    path('',AgentListView.as_view(),name='agents-page'),
    path('create/',AgentCreateView.as_view(),name='create-page'),
    path('<int:pk>/',AgentDetailView.as_view(),name='agent-page'),
    path('<int:pk>/update/',AgentUpdateView.as_view(),name='update-page'),
    path('<int:pk>/delete/',AgentDeleteView.as_view(),name='delete'),
]
