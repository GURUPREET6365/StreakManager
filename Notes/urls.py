from django.urls import path
from . import views

urlpatterns = [
    # Root folder view
    path('notes/', views.folder_list, name='folder_list'),
    
    # Specific folder view
    path('notes/folder/<int:folder_id>/', views.folder_list, name='folder_list'),
    
    # Create folder in root
    path('notes/create_folder/', views.create_folder, name='create_folder'),
    
    # Create folder inside another folder
    path('notes/create_folder/<int:parent_id>/', views.create_folder, name='create_folder'),
    
    # Upload file to root
    path('notes/upload/', views.upload_file, name='upload_file'),
    
    # Upload file to folder
    path('notes/upload/<int:folder_id>/', views.upload_file, name='upload_file'),
    
    # Delete folder
    path('notes/delete_folder/<int:folder_id>/', views.delete_folder, name='delete_folder'),

    # This is for changing the name of the folder.
    path('notes/edit_folder/<int:folder_id>/', views.edit_folder, name='edit_folder'),

    # Delete file for root 
    path('notes/delete_file/<int:file_id>/', views.delete_file, name='delete_file')    

]
