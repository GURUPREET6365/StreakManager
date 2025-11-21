// This script handles all drag-and-drop functionality and file validation
// It stores selected files in a Map to prevent duplicates and validate size/type

// Store selected files in a Map (filename as key to prevent duplicates)
const selectedFiles = new Map();

// Constants for validation
const MAX_FILE_SIZE = 20 * 1024 * 1024; // 20 MB in bytes
const ALLOWED_EXTENSIONS = ['pdf', 'jpg', 'jpeg', 'png'];

// Get DOM elements
const dropZone = document.getElementById('dropZone');
const fileInput = document.getElementById('fileInput');
const hiddenFileInput = document.getElementById('hiddenFileInput');
const selectedFilesContainer = document.getElementById('selectedFilesContainer');
const filesList = document.getElementById('filesList');
const fileCount = document.getElementById('fileCount');
const clearAllBtn = document.getElementById('clearAllBtn');
const uploadForm = document.getElementById('uploadForm');

// Prevent default drag behaviors on the entire document
['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
  document.body.addEventListener(eventName, preventDefaults, false);
});

function preventDefaults(e) {
  e.preventDefault();
  e.stopPropagation();
}

// Highlight drop zone when dragging over it
['dragenter', 'dragover'].forEach(eventName => {
  dropZone.addEventListener(eventName, highlight, false);
});

['dragleave', 'drop'].forEach(eventName => {
  dropZone.addEventListener(eventName, unhighlight, false);
});

function highlight(e) {
  dropZone.style.borderColor = '#38bdf8';
  dropZone.style.background = 'rgba(56,189,248,0.1)';
  dropZone.style.transform = 'scale(1.02)';
}

function unhighlight(e) {
  dropZone.style.borderColor = 'rgba(56,189,248,0.3)';
  dropZone.style.background = 'rgba(56,189,248,0.03)';
  dropZone.style.transform = 'scale(1)';
}

// Handle dropped files
dropZone.addEventListener('drop', handleDrop, false);

function handleDrop(e) {
  const dt = e.dataTransfer;
  const files = dt.files;
  handleFiles(files);
}

// Handle click to browse files
dropZone.addEventListener('click', () => {
  fileInput.click();
});

// Handle file selection from file input
fileInput.addEventListener('change', (e) => {
  handleFiles(e.target.files);
  // Reset the input so the same file can be selected again if removed
  e.target.value = '';
});

// Main function to handle selected files
function handleFiles(files) {
  // Convert FileList to Array
  const filesArray = Array.from(files);
  
  filesArray.forEach(file => {
    // Validate file type
    const fileExtension = file.name.split('.').pop().toLowerCase();
    if (!ALLOWED_EXTENSIONS.includes(fileExtension)) {
      showError(`${file.name} is not allowed. Only PDF, JPG, JPEG, PNG files are accepted.`);
      return;
    }
    
    // Validate file size
    if (file.size > MAX_FILE_SIZE) {
      showError(`${file.name} is too large. Maximum file size is 20MB.`);
      return;
    }
    
    // Check for duplicates (same filename)
    if (selectedFiles.has(file.name)) {
      showError(`${file.name} is already added.`);
      return;
    }
    
    // Add file to the Map
    selectedFiles.set(file.name, file);
  });
  
  // Update the UI
  updateFilesList();
  updateHiddenInput();
}

// Update the files list display
function updateFilesList() {
  if (selectedFiles.size === 0) {
    selectedFilesContainer.style.display = 'none';
    return;
  }
  
  selectedFilesContainer.style.display = 'block';
  fileCount.textContent = selectedFiles.size;
  
  // Clear the list
  filesList.innerHTML = '';
  
  // Add each file to the list
  selectedFiles.forEach((file, filename) => {
    const fileItem = createFileItem(file, filename);
    filesList.appendChild(fileItem);
  });
}

// Create a file item element
function createFileItem(file, filename) {
  const div = document.createElement('div');
  div.className = 'file-item';
  div.style.cssText = `
    background: rgba(30,41,59,0.8);
    border: 1px solid rgba(56,189,248,0.2);
    border-radius: 8px;
    padding: 0.75rem 1rem;
    margin-bottom: 0.5rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    transition: all 0.2s ease;
  `;
  
  // Get file icon based on extension
  const extension = filename.split('.').pop().toLowerCase();
  let icon = 'bi-file-earmark-fill';
  let iconColor = '#22c55e';
  
  if (extension === 'pdf') {
    icon = 'bi-file-earmark-pdf-fill';
    iconColor = '#ef4444';
  } else if (['jpg', 'jpeg', 'png'].includes(extension)) {
    icon = 'bi-file-earmark-image-fill';
    iconColor = '#a855f7';
  }
  
  div.innerHTML = `
    <div style="display: flex; align-items: center; gap: 0.75rem; flex: 1; min-width: 0;">
      <i class="bi ${icon}" style="font-size: 1.5rem; color: ${iconColor}; flex-shrink: 0;"></i>
      <div style="flex: 1; min-width: 0;">
        <p style="color: #cbd5e1; 
                  font-weight: 500; 
                  margin: 0; 
                  font-size: 0.875rem;
                  overflow: hidden;
                  text-overflow: ellipsis;
                  white-space: nowrap;" 
           title="${filename}">
          ${filename}
        </p>
        <small style="color: #64748b; font-size: 0.75rem;">
          ${formatFileSize(file.size)}
        </small>
      </div>
    </div>
    <button type="button" 
            class="btn btn-sm remove-file-btn"
            data-filename="${filename}"
            style="background: rgba(239,68,68,0.1);
                   border: 1px solid rgba(239,68,68,0.3);
                   color: #ef4444;
                   padding: 0.25rem 0.5rem;
                   flex-shrink: 0;
                   transition: all 0.2s ease;">
      <i class="bi bi-x-lg"></i>
    </button>
  `;
  
  // Add hover effect
  div.addEventListener('mouseenter', () => {
    div.style.background = 'rgba(30,41,59,1)';
    div.style.borderColor = 'rgba(56,189,248,0.4)';
  });
  
  div.addEventListener('mouseleave', () => {
    div.style.background = 'rgba(30,41,59,0.8)';
    div.style.borderColor = 'rgba(56,189,248,0.2)';
  });
  
  // Add remove button functionality
  const removeBtn = div.querySelector('.remove-file-btn');
  removeBtn.addEventListener('click', () => {
    selectedFiles.delete(filename);
    updateFilesList();
    updateHiddenInput();
  });
  
  // Hover effect for remove button
  removeBtn.addEventListener('mouseenter', () => {
    removeBtn.style.background = 'rgba(239,68,68,0.2)';
    removeBtn.style.borderColor = '#ef4444';
  });
  
  removeBtn.addEventListener('mouseleave', () => {
    removeBtn.style.background = 'rgba(239,68,68,0.1)';
    removeBtn.style.borderColor = 'rgba(239,68,68,0.3)';
  });
  
  return div;
}

// Format file size to human-readable format
function formatFileSize(bytes) {
  if (bytes === 0) return '0 Bytes';
  
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  
  return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + ' ' + sizes[i];
}

// Update hidden file input with selected files
function updateHiddenInput() {
  // Create a new DataTransfer object to hold files
  const dataTransfer = new DataTransfer();
  
  // Add all selected files to the DataTransfer object
  selectedFiles.forEach(file => {
    dataTransfer.items.add(file);
  });
  
  // Set the files property of the hidden input
  hiddenFileInput.files = dataTransfer.files;
}

// Clear all selected files
clearAllBtn.addEventListener('click', () => {
  selectedFiles.clear();
  updateFilesList();
  updateHiddenInput();
});

// Show error message
function showError(message) {
  // Create error alert
  const alertDiv = document.createElement('div');
  alertDiv.className = 'alert alert-danger alert-dismissible fade show';
  alertDiv.setAttribute('role', 'alert');
  alertDiv.style.cssText = `
    position: fixed;
    top: 20px;
    right: 20px;
    z-index: 9999;
    max-width: 400px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.3);
  `;
  
  alertDiv.innerHTML = `
    ${message}
    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
  `;
  
  document.body.appendChild(alertDiv);
  
  // Auto-remove after 5 seconds
  setTimeout(() => {
    alertDiv.remove();
  }, 5000);
}

// Handle form submission
uploadForm.addEventListener('submit', (e) => {
  if (selectedFiles.size === 0) {
    e.preventDefault();
    showError('Please select at least one file to upload.');
    return;
  }
  
  // Disable upload button to prevent double submission
  const uploadBtn = document.getElementById('uploadBtn');
  uploadBtn.disabled = true;
  uploadBtn.innerHTML = '<i class="bi bi-hourglass-split me-1"></i> Uploading...';
});