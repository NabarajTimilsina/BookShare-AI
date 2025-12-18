from django.shortcuts import render, redirect, get_object_or_404
from .models import Book
from utils.summariser import get_book_summary
import PyPDF2


def home(request):
    books = Book.objects.all()
    return render(request, 'books/home.html', {'books': books})


def upload_book(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        author = request.POST.get('author', '').strip()
        pdf_file = request.FILES.get('pdf_file')

        if not title or not author or not pdf_file:
            return render(request, 'books/upload.html', {
                'error': 'Please fill all fields and upload a PDF.'
            })

        # STEP 1 — Extract text from PDF
        try:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ""

            for page in pdf_reader.pages:
                extracted = page.extract_text() or ""
                text += extracted

            if not text.strip():
                text = f"Could not extract readable text from '{title}'"

        except Exception as e:
            text = f"PDF reading error: {str(e)}"

        # STEP 2 — AI Summary (Hugging Face)
        summary = get_book_summary(text)
        print("📄 TEXT LENGTH:", len(text))
        print("📄 TEXT SAMPLE:", text[:500])


        # STEP 3 — Save book
        Book.objects.create(
            title=title,
            author=author,
            summary=summary,
            pdf_file=pdf_file
        )

        return redirect('home')

    return render(request, 'books/upload.html')


def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'books/detail.html', {'book': book})


def search_books(request):
    query = request.GET.get('q', '').strip()

    if not query:
        return render(request, 'books/search.html', {
            'results': [],
            'query': query
        })

    results = Book.objects.filter(title__icontains=query)

    return render(request, 'books/search.html', {
        'results': results,
        'query': query
    })
def ajax_search(request):
    query = request.GET.get('q', '').strip()
    if not query:
        return JsonResponse({'results': []})

    results = list(Book.objects.filter(title__icontains=query).values('id', 'title', 'author'))
    return JsonResponse({'results': results})
