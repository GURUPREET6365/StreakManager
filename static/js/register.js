let eye_button1 = document.getElementById('togglePassword1')

let password1 = document.getElementById('id_password1')

// Accessing the eye buttton to change.
eye1 = document.getElementById('eyeIcon1')

eye_button1.addEventListener('click', function(){
    
    if (password1.type === 'password') {
        password.type = 'text';
        eye1.classList.replace('bi-eye-slash', 'bi-eye')        
    }
    else  {
        password1.type = 'password';
        eye1.classList.replace('bi-eye', 'bi-eye-slash')        
    }

} )


// This is for the second password
let eye_button2 = document.getElementById('togglePassword2')

let password2 = document.getElementById('id_password2')

// Accessing the eye buttton to change.
eye2 = document.getElementById('eyeIcon2')

eye_button2.addEventListener('click', function(){
    
    if (password2.type === 'password') {
        password2.type = 'text';
        eye2.classList.replace('bi-eye-slash', 'bi-eye')        
    }
    else  {
        password2.type = 'password';
        eye2.classList.replace('bi-eye', 'bi-eye-slash')        
    }

} )