from django.db import models
from django.contrib.auth.models import User


class Folder(models.Model):
    # Giving the name column for taking the name of the folder provided by the user.
    name = models.CharField(max_length=255)

    # Making the parent variable for naming the parent folder with foreignkey which will tell that it's parent is another.
    # And foreignkey is always an id. and we will use id to give the parent.
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name = 'sub_folder')
    # We gave related_name to access it's subfoder, if it will have.


    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='folder')

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateField(blank=True, null=True)

    class Meta:
        ordering = ['name']
    # We created this meta class for giving them meta data to the model we created so that when we will access this, this meta data will also provided like in this ordering will provided and it will be ordered by name.

        unique_together = ['name', 'parent', 'owner']
        # This will ensure that the folder name should be uniques in the parent and for that owner.

    def __str__(self):
        return self.name
    # This will show the name of the folder in django admin panel.

    def get_full_path(self):
        # making a path variable.
        path = [self.name] # We used the bracket because we are making the path of the folder's.

        parent = self.parent
        # We are taking the id of the parent we created in the model that is also known as pk.

        # Now making a loop so that if the file id is none the it will stop so that we can send the user to any path.
        while parent is not None:

            path.append(parent.name)
            parent = parent.parent
            
            # Now using the recursive feature of the path list because it is now from child to parent but we want parent to child.
        path.reverse()
        return '/'.join(path) # This will join the path with the string '/'.
        
        # Now we will check that is the user is in root folder.
    def is_root(self):
        return self.parent is None
    
    # This is for getting all the childrend of the folder.
    def get_all_children(self):
        sub_folder=[]
        for child in self.sub_folder.all():
            sub_folder.append(child)
            sub_folder.extend(child.get_all_children())

        return sub_folder
        


# This is for the custom path to where to save the file.
def filePath(instance, filename):
    user = instance.owner # NOTE: That this instance.owner gives you the actual user object in which contains all the information about the user like name, id, email, username, last name, etc.
    return f"Notes/{user.id}/{user.username}/{filename}"



class File(models.Model):
    name = models.CharField(max_length=255)

    file = models.FileField(upload_to=filePath)
    # WHY upload_to='drive_files/%Y/%m/%d/'? 
    #   - Organizes files by date: drive_files/2024/11/18/resume.pdf

    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name='files', null=True, blank=True)

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users_notes')

    # This is for file size.
    size = models.BigIntegerField()

    mime_type = models.CharField(max_length=100, blank=True)
    # This is used for storing the file type like pdf, jpg, etc.

    created_at = models.DateTimeField(auto_now_add=True)

    update_at = models.DateField(blank=True, null=True)

    class Meta:
        ordering=['-created_at']
        # This is for ordering the file by the created date, and also '-' represent that from newest to oldest, means descending order.
    
    def __str__(self):
        return self.name

    # This is for the taking the file extension.
    def get_file_extension(self):
        import os
        return os.path.splitext(self.name)[1][1:] # It makes the tuple 
        # filename = "example.document.pdf"
        # root, ext = os.path.splitext(filename)
        # print(root)  # Output: example.document
        # print(ext)   # Output: .pdf
        # print(ext[1:])  # Output: pdf

    def get_human_readable_size(self):
        size = self.size

        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return f'{size:.2f} {unit}'
            size /= 1024.0