let eyebutton1 = document.getElementById('toggleOld')

let oldpassword1 = document.getElementById('oldpassword')

eyeIcon1 = document.getElementById('iconOld')

eyebutton1.addEventListener('click', function(){
    if (oldpassword1.type == 'password'){
        oldpassword1.type = 'text';
        eyeIcon1.classList.replace('bi-eye-slash', 'bi-eye')        

    }
    else  {
        oldpassword1.type = 'password';
        eyeIcon1.classList.replace('bi-eye', 'bi-eye-slash')        
    }
})

let eyebutton2 = document.getElementById('toggleNew1')

let newpassword1 = document.getElementById('newpassword1')

eyeIcon2 = document.getElementById('iconNew1')

eyebutton2.addEventListener('click', function(){
    if (newpassword1.type == 'password'){
        newpassword1.type = 'text';
        eyeIcon2.classList.replace('bi-eye-slash', 'bi-eye')        

    }
    else  {
        newpassword1.type = 'password';
        eyeIcon2.classList.replace('bi-eye', 'bi-eye-slash')        
    }
})

let eyebutton3 = document.getElementById('toggleNew2')

let newpassword2 = document.getElementById('newpassword2')

eyeIcon3 = document.getElementById('iconNew2')

eyebutton3.addEventListener('click', function(){
    if (newpassword2.type == 'password'){
        newpassword2.type = 'text';
        eyeIcon3.classList.replace('bi-eye-slash', 'bi-eye')        

    }
    else  {
        newpassword2.type = 'password';
        eyeIcon3.classList.replace('bi-eye', 'bi-eye-slash')        
    }
})


// This is for the edit email in the profile page for showing otp 
const sendOtpBtn = document.getElementById("sendOtpBtn");
const emailInput = document.getElementById("email");
const otpBox = document.getElementById("otpBox");
const saveBtn = document.getElementById("saveBtn");
const verifyOtpBtn = document.getElementById("verifyOtpBtn");

sendOtpBtn.addEventListener("click", function() {

let email = emailInput.value;

if (!email) {
    alert("Please enter an email.");
    return;
}

// TODO: Here you will send AJAX to backend to send OTP

// Show OTP box
otpBox.style.display = "block";

// Disable email field
emailInput.readOnly = true;

// Hide Save button
saveBtn.style.display = "none";

// Hide Send OTP button
sendOtpBtn.style.display = "none";

// Show Verify OTP button
verifyOtpBtn.style.display = "inline-block";
});
