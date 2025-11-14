let eye_button1 = document.getElementById('togglePassword1')

let password1 = document.getElementById('id_password1')

// Accessing the eye buttton to change.
eye1 = document.getElementById('eyeIcon1')

eye_button1.addEventListener('click', function(){
    
    if (password1.type === 'password') {
        password1.type = 'text';
        eye1.classList.replace('bi-eye-slash', 'bi-eye')        
    }
    else  {
        password1.type = 'password';
        eye1.classList.replace('bi-eye', 'bi-eye-slash')        
    }

} )
