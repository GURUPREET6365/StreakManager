from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Folder, File



# Create your views here.


# This is for folder list
@login_required
def folder_list(request, folder_id = None):
    user = request.user

    # determining the current folder, as if the folder_id is none then it will be parent folder and then it is handled by this views.
    if folder_id:
        current_folder = get_object_or_404(Folder, id=folder_id, owner=user)


    else:
        current_folder=None
    
    if current_folder:
        folders = Folder.objects.filter(parent=current_folder, owner=user)
    
    else:
        folders = Folder.objects.filter(parent=None, owner=user)

    files = File.objects.filter(folder=current_folder, owner=user).order_by('-created_at')

    breadcrumbs = []
    if current_folder:
        temp = current_folder
        while temp:
            breadcrumbs.insert(0, temp)  # Add to beginning
            temp = temp.parent
    # Result: [My Drive, Work, Projects] for Projects folder
    context = {
        'current_folder':current_folder,
        'folders':folders,
        'files':files,
        'breadcrumbs':breadcrumbs
    }
    return render(request, 'Notes/notes.html', context)

@login_required
def create_folder(request, parent_id=None):
    """Create a new folder"""
    if request.method == 'POST':
        folder_name = request.POST.get('folder_name')
        
        # Validation
        if not folder_name:
            messages.error(request, "Folder name is required")
            # FIX: Redirect conditionally
            if parent_id:
                return redirect('folder_list', folder_id=parent_id)
            else:
                return redirect('folder_list')
        
        # Get parent folder (if creating inside another folder)
        parent_folder = None
        if parent_id:
            parent_folder = get_object_or_404(Folder, id=parent_id, owner=request.user)
        
        # Check for duplicate names
        existing = Folder.objects.filter(
            name=folder_name,
            parent=parent_folder,
            owner=request.user
        ).exists()
        
        if existing:
            messages.error(request, f"Folder '{folder_name}' already exists here")
            # FIX: Redirect conditionally
            if parent_id:
                return redirect('folder_list', folder_id=parent_id)
            else:
                return redirect('folder_list')
        
        # Create the folder
        Folder.objects.create(
            name=folder_name,
            parent=parent_folder,
            owner=request.user
        )
        
        messages.success(request, f"Folder '{folder_name}' created successfully")
        
        # FIX: Redirect conditionally - THIS IS THE KEY FIX!
        if parent_id:
            return redirect('folder_list', folder_id=parent_id)
        else:
            return redirect('folder_list')
    
    return redirect('folder_list')



@login_required
def upload_file(request, folder_id=None):
    """
    Upload a file to a folder
    """
    if request.method == 'POST':
        # NOTE: This is the below code where we take file send by the user, but this only takes one file, when we send the multiple files, then html send it as a list.
        # uploaded_file = request.FILES['file']
        
        uploaded_file = request.FILES.getlist("file")

        # Get folder to upload into
        folder = None
        if folder_id:
            folder = get_object_or_404(Folder, id=folder_id, owner=request.user)
        

        for files in uploaded_file:
            filename = files.name

            filesize = files.size
            # Checking the file existance
            exists_file = File.objects.filter(
            name=filename, # Django handles storage
            folder=folder,
            owner=request.user,  # Get file size in bytes
            mime_type=files.content_type,  # Get MIME type
        )
            if exists_file.exists():
                messages.info(request, f"{exists_file.first().name}")
                if folder_id:
                    return redirect('folder_list', folder_id=folder_id)
                else:
                    return redirect('folder_list')
            
            else:
                file_obj = File.objects.create(
                name=filename,
                file=files,  # Django handles storage
                folder=folder,
                owner=request.user,
                size=filesize,  # Get file size in bytes
                mime_type=files.content_type  # Get MIME type
                                                )
                messages.success(request, f"File '{filename}' uploaded successfully")
        if folder_id:
            return redirect('folder_list', folder_id=folder_id)
        else:
            return redirect('folder_list')
    
        
        
        
        
    return redirect('folder_list', folder_id=folder_id)


@login_required
def delete_folder(request, folder_id):
    """
    Delete a folder (and everything inside it due to CASCADE)
    """
    if request.method == 'POST':
        user = request.user
        folder = get_object_or_404(Folder, pk=folder_id, owner=user)
        parent_id = folder.parent_id # When we use foreign key then the name of the column we are giving uske aage hi _id lag jata hai. isiliye ham id se acceess karte hia.

        folder.delete()
        if parent_id:
            return redirect('folder_list', folder_id=parent_id)
        else:
            return redirect('folder_list') 
        
@login_required
def edit_folder(request, folder_id):
    if request.method == 'POST':
        user = request.user
        new_folder = request.POST.get('new_folder_name')
        folder = get_object_or_404(Folder, pk=folder_id, owner=user)
        if new_folder == folder.name:
            messages.info(request, 'New name of the folder should be different from previous.')
        folder.name=new_folder
        folder.save()
        parent= folder.parent_id
        if parent:
            return redirect('folder_list', folder_id=parent)
        else:
            return redirect('folder_list')

@login_required
def delete_file(request, file_id):
    if request.method == 'POST':
        owner = request.user
        file = get_object_or_404(File, id=file_id, owner=owner)
        # NOTE: why we did folder_id. Because in the model of File there is folder named column, which is linked with the foreign key of the model Folder, so as it is the foreignkey, then djngo will give the name of the column in hte database as folder_id.
        folder_id = file.folder_id
        # Delete physical file
        file.file.delete(save=False)
        file.delete()
        
        if folder_id:
            return redirect('folder_list', folder_id = folder_id)
        else:
            return redirect('folder_list')