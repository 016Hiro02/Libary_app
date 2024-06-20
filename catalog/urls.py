from django.urls import re_path , include
from . import views

urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    re_path(r'^books/$', views.BookListView.as_view(), name='books'),
    re_path(r'^book/(?P<pk>\d+)$', views.BookDetailView, name='book-detail'),
    re_path(r'^authors/$', views.AuthorListView.as_view(), name='authors'),
    re_path(r'^author/(?P<pk>\d+)$', views.AuthorDetailView, name='author-detail'),
    re_path(r'^meme/$', views.meme, name='meme'),
    re_path(r'^mybooks/$', views.LBBULV.as_view(), name='my-borrowed'),
    re_path(r'^libM/$', views.libM, name='libM')
]

urlpatterns += [
    re_path(r'^book_instances/$', views.BookInstanceListView.as_view(), name='bookinstances'),
    re_path(r'^genres/$', views.GenreListView.as_view(), name='genres'),
]

urlpatterns += [
    re_path(r'^book/(?P<pk>[-\w]+)/renew/$', views.renew_book_librarian, name='renew-book-librarian'),
]

urlpatterns += [
    re_path(r'^author/create/$', views.AuthorCreate.as_view(), name='author_create'),
    re_path(r'^author/(?P<pk>\d+)/update/$', views.AuthorUpdate.as_view(), name='author_update'),
    re_path(r'^author/(?P<pk>\d+)/delete/$', views.AuthorDelete.as_view(), name='author_delete'),
]

urlpatterns += [
    re_path(r'^book/create/$', views.BookCreate.as_view(), name='book_create'),
    re_path(r'^book/(?P<pk>\d+)/update/$', views.BookUpdate.as_view(), name='book_update'),
    re_path(r'^book/(?P<pk>\d+)/delete/$', views.BookDelete.as_view(), name='book_delete'),
]

urlpatterns += [
    re_path(r'^genres/create/$', views.GenreCreate.as_view(), name='genre_create'),
    re_path(r'^genres/(?P<pk>\d+)/update/$', views.GenreUpdate.as_view(), name='genre_update'),
    re_path(r'^genres/(?P<pk>\d+)/delete/$', views.GenreDelete.as_view(), name='genre_delete'),
]

urlpatterns += [
    re_path(r'^book_instance/create/$', views.BookInstanceCreate.as_view(), name='bookinstance_create'),
    re_path(r'^book_instance/(?P<pk>[-\w]+)/update/$', views.BookInstanceUpdate.as_view(), name='bookinstance_update'),
    re_path(r'^book_instance/(?P<pk>[-\w]+)/delete/$', views.BookInstanceDelete.as_view(), name='bookinstance_delete'),
]


urlpatterns += [
    re_path(r'^bookinst/(?P<pk>[-\w]+)/fokus/$', views.fokus.as_view(), name='fokus'),
    re_path(r'^bookinst/(?P<pk>[-\w]+)/fokus2/$', views.fokus2, name='fokus2'),
]