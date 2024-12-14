from django.urls import path
from .views import ProcessInstructionView

urlpatterns = [
    path('process-instruction/', ProcessInstructionView.as_view(), name='process-instruction'),
]
