from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Book
from .forms import BookForm
from django.contrib.auth import authenticate, login
import pdf2image
from django.contrib.auth import logout
from django.core.paginator import Paginator
import gensim
from gensim import corpora

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error': 'Username atau password salah!'})
    return render(request, 'login.html')

@login_required
def dashboard(request):
    books = Book.objects.all()
    return render(request, 'dashboard.html', {'books': books})

@login_required
def book_list(request):
    query = request.GET.get('query', '')
    if query:
        books = Book.objects.filter(title__icontains=query)
    else:
        books = Book.objects.all()

    paginator = Paginator(books, 10)  # Show 10 books per page
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)

    return render(request, 'book_list.html', {
        'books': page_obj,
        'query': query,
        'query_params': f"&query={query}" if query else '',
        'page_obj': page_obj,
    })

@login_required
def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'book_detail.html', {'book': book})

@login_required
def book_create(request):
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = BookForm()
    return render(request, 'book_form.html', {'form': form})

@login_required
def book_update(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = BookForm(instance=book)
    return render(request, 'book_form.html', {'form': form})

@login_required
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    book.delete()
    return redirect('dashboard')

@login_required
def pdf_preview(request, pk):
    from pdf2image import convert_from_path
    book = get_object_or_404(Book, pk=pk)
    if book.pdf_file:
        images = convert_from_path(book.pdf_file.path)
        return render(request, 'pdf_preview.html', {'images': images})
    return redirect('book_detail', pk=pk)

def Logout(request):
    logout(request)
    return redirect ("/")

def topic_modeling(request):
    books = Book.objects.all()
    texts = [book.description.split() for book in books if book.description]  # Only include books with descriptions
    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]
    
    # Train the LDA model
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=5, id2word=dictionary, passes=15)
    topics = ldamodel.print_topics(num_words=4)
    
    return render(request, 'topic.html', {'topics': topics})