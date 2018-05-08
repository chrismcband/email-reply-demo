from django.conf.urls import url

from . import views

app_name = "emails"
urlpatterns = [
    url(regex=r"^$", view=views.EmailListView.as_view(), name="list"),
    url(regex=r"^parse/$", view=views.parse, name="parse"),
    url(regex=r"^create/$", view=views.EmailCreateView.as_view(),
        name="create"),
    url(
        regex=r"^(?P<id>\d+)/$",
        view=views.EmailDetailView.as_view(),
        name="detail",
    ),
]
