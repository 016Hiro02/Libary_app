from django.shortcuts import render, get_object_or_404, redirect
from django import forms
from .models import Book, Author, BookInstance, Genre
from django.views import generic
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime
from .forms import RenewBookForm
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Author



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

class BookInstanceListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance

    paginate_by = 5

    template_name= '/Libary_app/catalog/templates/book_instance_list.html'
    
    def get_context_data(self, **kwargs):
        context = super(BookInstanceListView, self).get_context_data(**kwargs)
        context['some_data'] = 'This is just some data'
        return context

class GenreListView(LoginRequiredMixin, generic.ListView):
    model = Genre
    paginate_by = 6
    template_name= '/Libary_app/catalog/templates/genre_list.html'
    def get_context_data(self, **kwargs):
        context = super(GenreListView, self).get_context_data(**kwargs)
        context['some_data'] = 'This is just some data'
        return context


def meme(request):
    bebra = 'imma firin mah laser'
    return render(request, 'meme.html', context={'bebra':bebra,})

class LBBULV(LoginRequiredMixin,generic.ListView):

    model = BookInstance
    template_name ='/Libary_app/catalog/templates/borow.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

class res(LoginRequiredMixin,generic.ListView):

    model = BookInstance
    template_name ='/Libary_app/catalog/templates/reserved.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='r').order_by('due_back')

@permission_required('catalog.can_mark_returned')
def libM(request):
    bookinst = BookInstance.objects.filter(status__exact='o').order_by('due_back')
    return render(request, 'libM.html', context={'bookinstance_list':bookinst})

@permission_required('catalog.change_bookinstance')
def libR(request):
    bookinst = BookInstance.objects.filter(status__exact='r').order_by('due_back')
    return render(request, 'libR.html', context={'bookinstance_list':bookinst})

def approveBook(request, pk):
    bookinst = get_object_or_404(BookInstance, pk=pk)
    bookinst.due_back= datetime.date.today() + datetime.timedelta(weeks=3)
    bookinst.status= 'o'
    bookinst.borrower = request.user
    bookinst.save()
    back_url = request.META["HTTP_REFERER"] or request.path

    return redirect(back_url)

@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    book_inst = get_object_or_404(BookInstance, pk=pk)

    if request.method == 'POST':

        form = RenewBookForm(request.POST)

        if form.is_valid():
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()

            return HttpResponseRedirect(reverse('libM') )

    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date,})

    return render(request, 'book_renew_librarian.html', {'form': form, 'bookinst':book_inst})

class AuthorCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('catalog.create_author')
    model = Author
    fields = '__all__'
    template_name ='/Libary_app/catalog/templates/author_form.html'
    success_url = reverse_lazy('authors')

class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('catalog.change_author')
    model = Author
    fields = ['first_name','last_name','date_of_birth','date_of_death']
    template_name ='/Libary_app/catalog/templates/author_form.html'
    success_url = reverse_lazy('authors')

class AuthorDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('catalog.delete_author')
    model = Author
    success_url = reverse_lazy('authors')
    template_name ='/Libary_app/catalog/templates/author_confirm_delete.html'

class BookCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('catalog.create_book')
    model = Book
    fields = '__all__'
    template_name ='/Libary_app/catalog/templates/Book_form.html'
    success_url = reverse_lazy('books')

class BookUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('catalog.change_book')
    model = Book
    fields = '__all__'
    template_name ='/Libary_app/catalog/templates/Book_form.html'
    success_url = reverse_lazy('books')

class BookDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('catalog.delete_book')
    model = Book
    success_url = reverse_lazy('books')
    template_name ='/Libary_app/catalog/templates/Book_confirm_delete.html'

class BookInstanceCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('catalog.create_bookinstance')
    model = BookInstance
    fields = '__all__'
    template_name ='/Libary_app/catalog/templates/BookInstance_form.html'
    success_url = reverse_lazy('booksbookinstances')

class BookInstanceUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('catalog.change_bookinstance')
    model = BookInstance
    fields = '__all__'
    template_name ='/Libary_app/catalog/templates/BookInstance_form.html'
    success_url = reverse_lazy('booksbookinstances')

class BookInstanceDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('catalog.delete_bookinstance')
    model = BookInstance
    success_url = reverse_lazy('booksbookinstances')
    template_name ='/Libary_app/catalog/templates/BookInstance_confirm_delete.html'

class GenreCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('catalog.create_genre')
    model = Genre
    fields = '__all__'
    template_name ='/Libary_app/catalog/templates/genre_form.html'
    success_url = reverse_lazy('Genres')

class GenreUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('catalog.change_genre')
    model = Genre
    fields = '__all__'
    template_name ='/Libary_app/catalog/templates/genre_form.html'
    success_url = reverse_lazy('Genres')

class GenreDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('catalog.delete_genre')
    model = Genre
    success_url = reverse_lazy('Genres')
    template_name ='/Libary_app/catalog/templates/genre_confirm_delete.html'



'''
@permission_required('catalog.can_mark_returned')
def fokus(request, pk):
    bookinst = get_object_or_404(BookInstance, pk=pk)
    bookinst.due_back= None
    bookinst.status= 'a'
    bookinst.borrower = None
    bookinst.save()
    return render(request, 'libM.html', {'bookinst':bookinst,})

'''
class fokus(PermissionRequiredMixin, UpdateView):
    permission_required = ('catalog.can_mark_returned', 'catalog.change_bookinstance')
    model = BookInstance
    fields = ['borrower', 'due_back','status',]
    template_name ='/Libary_app/catalog/templates/fokus.html'
    success_url = reverse_lazy('libM')
    initial={'due_back':None,'status':'a','borrower':None}


def fokus2(request, pk):
    bookinst = get_object_or_404(BookInstance, pk=pk)
    bookinst.due_back= datetime.date.today() + datetime.timedelta(weeks=2)
    bookinst.status= 'r'
    bookinst.borrower = request.user
    bookinst.save()
    back_url = request.META["HTTP_REFERER"] or request.path

    return redirect(back_url)
