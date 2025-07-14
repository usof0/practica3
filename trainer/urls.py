from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('', views.review_words, name='review'),
    path('word-list/', views.word_list, name='word-list'),
    path('add/', views.add_word, name='add-word'),
    path('mark-learned/<int:word_id>/', views.mark_learned, name='mark-learned'),
    path('import/', views.import_words, name='import-words'),
    path('import/sample/', views.download_sample_csv, name='download-sample-csv'),
    path('word/edit/<int:word_id>/', views.edit_word, name='edit-word'),
]