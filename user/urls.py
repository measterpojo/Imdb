from django.urls import path

from .views import (UserProfile, ReviewDetail,
    like, unlike)

from .views import (Signup, PasswordChange, PasswordChangeDone, EditProfile)

from django.contrib.auth import views as authViews

urlpatterns = [
    path('<username>', UserProfile, name='profile'),
    path('<username>/review/<imdb_id>', ReviewDetail, name='user-review'),
    path('<username>/review/<imdb_id>/like', like, name='user-review-like'),
    path('<username>/review/<imdb_id>/unlike', unlike, name='user-review-unlike'),



    path('editprofile/', EditProfile, name='edit-profile'),
    path('signup/', Signup, name='signup'),
    path('login/', authViews.LoginView.as_view(), name='login'),
    path('logout/', authViews.LogoutView.as_view(), {'next_page': 'login'}, name='logout'),
	path('changepassword/', PasswordChange, name='change-password'),
	path('changepassword/done', PasswordChangeDone, name='change-password-done'),
	path('passwordreset/', authViews.PasswordResetView.as_view(), name='password_reset'),
	path('passwordreset/done', authViews.PasswordResetDoneView.as_view(), name='password_reset_done'),
	path('passwordreset/<uidb64>/<token>/', authViews.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
	path('passwordreset/complete', authViews.PasswordResetCompleteView.as_view(), name='password_reset_complete'),   

]