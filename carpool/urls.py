from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.template, name='index'),
    path('search', views.SearchView.pesquisa, name='search'),
    path('create_carona',
         views.create_caronaView.as_view(), name='create_carona'),
    path('<int:pk>/edit_carona', views.edit_caronaView.as_view(), name='edit_carona'),
    path('userMessage', views.UserMessageView.as_view(), name='userMessage'),
    path('carona/<int:id>/member', views.AddMember.template,
         name='add_member_template'),
    path('member/add', views.AddMember.add, name='add_member'),
    path('listMessages/<int:active>',
         views.ListMessagesView.as_view(), name='listMessages'),
    path('listGroups', views.ListGroupsView.as_view(), name='listGroups'),
    path('<int:pk>/details', views.DetalharCarona.template, name='detail_carona'),
    path('account/new', views.UserView.template,
         name='create_account_template'),
    path('create_account', views.UserView.create, name='create_account'),
    path('accounts/login/', views.LoginUserView.template, name='login_template'),
    path('login', views.LoginUserView.login, name='login'),
    path('logout', views.LoginUserView.logout, name='logout')
]
