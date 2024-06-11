from django.shortcuts import render, get_object_or_404
from .models import Book, Author, BookInstance, Genre
from django.views import generic

def index(request):
    num_books=Book.objects.all().count()
    num_instances=BookInstance.objects.all().count()
    num_instances_available=BookInstance.objects.filter(status__exact='a').count()
    num_authors=Author.objects.count()  
    return render(request,
        'index.html',
        context={'num_books':num_books,'num_instances':num_instances,'num_instances_available':num_instances_available,'num_authors':num_authors,})

class BookListView(generic.ListView):
    model = Book

    paginate_by = 4

    template_name= '/Libary_app/catalog/templates/book_list.html'
    
    def get_context_data(self, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)
        context['some_data'] = 'This is just some data'
        return context

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

class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 3
    template_name= '/Libary_app/catalog/templates/author_list.html'
    def get_context_data(self, **kwargs):
        context = super(AuthorListView, self).get_context_data(**kwargs)
        context['some_data'] = 'This is just some data'
        return context

def AuthorDetailView(request,pk):

    author_id=get_object_or_404(Author, pk=pk)

    return render(
        request,
        'author_detail.html',
        context={'author':author_id,})