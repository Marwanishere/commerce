from django.urls import path
#2 imports below and corresponding static made using cs50 chatbot help
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("new_listing", views.new_listing_view, name="new_listing"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("bid/<int:listing_id>", views.current_price, name="current_price"),
    path("listing/<int:listing_id>", views.listing_view, name="listing")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
