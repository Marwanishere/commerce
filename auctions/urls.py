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
    path("listing/<int:listing_id>", views.listing_view, name="listing"),
    path("auction_closed/<int:listing_id>", views.closing_bid_view, name="auction_closed"),
    path("not_in", views.not_in, name = "not_in"),
    path("watch/1", views.watch, name = "watch"),
    path("categories", views.categories, name = "categories"),
    #ammendment to path below made using cs50 chatbot assistance
    path('category/<str:category>', views.category_view, name='category'),
    path('watch/<int:listing_id>/', views.a2w, name='a2w'),
    path("previous_listings", views.previous_listings_view, name = "previous_listings")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
