from django.shortcuts import render, get_object_or_404
from .models import Book, Author, BookInstance, Genre
from django.views import generic
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

@login_required
def index(request):

    num_books=Book.objects.all().count()
    num_instances=BookInstance.objects.all().count()
    num_instances_available=BookInstance.objects.filter(status__exact='a').count()
    num_authors=Author.objects.count()
    '''
    request.session['num_visits'] = 0
    request.session.modified = True
    '''
    num_visits=request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1
    return render(request,
        'index.html',
        context={'num_books':num_books,'num_instances':num_instances,'num_instances_available':num_instances_available,'num_authors':num_authors, 'num_visits':num_visits,})


class BookListView(LoginRequiredMixin, generic.ListView):
    model = Book

    paginate_by = 4

    template_name= '/Libary_app/catalog/templates/book_list.html'
    
    def get_context_data(self, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)
        context['some_data'] = 'This is just some data'
        return context

@login_required
def BookDetailView(request,pk):
    '''
    try:
        book_id=Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        raise Http404("Book does not exist")
    '''
    
    book_id=get_object_or_404(Book, pk=pk)

    return render(
        request,
        'book_detail.html',
        context={'book':book_id,})


class AuthorListView(LoginRequiredMixin, generic.ListView):
    model = Author
    paginate_by = 3
    template_name= '/Libary_app/catalog/templates/author_list.html'
    def get_context_data(self, **kwargs):
        context = super(AuthorListView, self).get_context_data(**kwargs)
        context['some_data'] = 'This is just some data'
        return context

@login_required
def AuthorDetailView(request,pk):

    author_id=get_object_or_404(Author, pk=pk)

    return render(
        request,
        'author_detail.html',
        context={'author':author_id,})

def meme(request):
    bebra = 'imma firin mah laser'
    return render(request, 'meme.html', context={'bebra':bebra,})

class LBBULV(LoginRequiredMixin,generic.ListView):

    model = BookInstance
    template_name ='/Libary_app/catalog/templates/borow.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

@permission_required('catalog.can_mark_returned')
@permission_required('catalog.can_edit')
def libM(request):
    bookinst = BookInstance.objects.filter(status__exact='o').order_by('due_back')
    return render(request, 'libM.html', context={'bookinstance_list':bookinst})
