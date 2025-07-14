from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import login


from .models import Word
from .forms import WordForm, WordImportForm, WordEditForm, RegisterForm
import csv

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Optional: log the user in immediately
            messages.success(request, "Registration successful!")
            return redirect('word-list')  # Redirect to your desired page
    else:
        form = RegisterForm()
    return render(request, 'trainer/register.html', {'form': form})

@login_required
def word_list(request):
    words = Word.objects.filter(user=request.user)
    words_learned_count = Word.objects.filter(user=request.user, is_learned=True).count()  # Add this line
    
    context = {
        'words': words,
        'words_learned_count': words_learned_count,  # Add this to context
    }
    return render(request, 'trainer/word_list.html', context)
# def word_list(request):
#     words = Word.objects.filter(user=request.user)
#     return render(request, 'trainer/word_list.html', {'words': words})


@login_required
def add_word(request):
    if request.method == 'POST':
        form = WordForm(request.POST)
        if form.is_valid():
            word = form.save(commit=False)
            word.user = request.user
            word.save()
            messages.success(request, 'Word added successfully!')
            return redirect('word-list')
    else:
        form = WordForm()
    return render(request, 'trainer/add_word.html', {'form': form})


@login_required
def review_words(request):
    words_to_review = Word.objects.filter(
        user=request.user,
        is_learned=False
    ).order_by('?')  # Random order for review
    
    if not words_to_review.exists():
        messages.info(request, 'No words to review! Add some words first.')
        return redirect('word-list')
    
    return render(request, 'trainer/review.html', {'word': words_to_review.first()})


@login_required
def mark_learned(request, word_id):
    word = get_object_or_404(Word, id=word_id, user=request.user)
    word.is_learned = True
    word.save()
    messages.success(request, f'Marked "{word.english}" as learned!')
    return redirect('review')

@login_required
def import_words(request):
    if request.method == 'POST':
        form = WordImportForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                csv_file = request.FILES['csv_file']
                decoded_file = csv_file.read().decode('utf-8').splitlines()
                reader = csv.DictReader(decoded_file)
                
                words_created = 0
                for row in reader:
                    Word.objects.create(
                        user=request.user,
                        english=row.get('english', '').strip(),
                        translation=row.get('translation', '').strip(),
                        example=row.get('example', '').strip(),
                        is_learned=False
                    )
                    words_created += 1
                
                messages.success(request, f'Successfully imported {words_created} words!')
                return redirect('word-list')
                
            except Exception as e:
                messages.error(request, f'Error importing file: {str(e)}')
    else:
        form = WordImportForm()
    
    return render(request, 'trainer/import_words.html', {'form': form})

@login_required
def download_sample_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="sample_words.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['english', 'translation', 'example'])
    writer.writerow(['apple', 'manzana', 'I eat an apple every morning'])
    writer.writerow(['book', 'libro', 'This book is very interesting'])
    writer.writerow(['computer', 'computadora', 'I work on my computer all day'])
    
    return response

@login_required
def edit_word(request, word_id):
    word = get_object_or_404(Word, id=word_id, user=request.user)
    
    if request.method == 'POST':
        form = WordEditForm(request.POST, instance=word)
        if form.is_valid():
            form.save()
            messages.success(request, 'Word updated successfully!')
            return redirect('word-list')
    else:
        form = WordEditForm(instance=word)
    
    return render(request, 'trainer/edit_word.html', {'form': form, 'word': word})