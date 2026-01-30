from django.urls import path

from .views import ArticleView, ReportView

urlpatterns = [
    path("articles/", ArticleView.as_view()),
    path("reports/", ReportView.as_view()),
]
