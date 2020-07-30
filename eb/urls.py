from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('user/', views.userpage, name="user-page"),
    path('maid/', views.maid, name="bai"),
    path('user-account/', views.accountu, name="u-acc"),
    path('user-history/', views.historyl, name="u-history"),
    path('book/<str:id>/', views.book, name="book"),
    path('details/<str:id>/', views.details, name="details"),
    path('wishlist/', views.wishlistl, name="wishlist"),
    path('wishlist-user/', views.wishlistli, name="wishlist-user"),

    path('login/', views.loginUser, name="login"),
    path('register/', views.registerUser, name="register"),
    path('logout/', views.logoutUser, name="logout"),

    path('Confirmation/', views.surity, name="surity"),
    path('worker/', views.workerr, name="worker"),
    path('Dashboard/', views.board, name="board"),
    path('maid-page/', views.home1, name="maid-page"),
    path('account-maid/', views.accountm, name="maid-account"),
]
