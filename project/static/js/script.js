document.addEventListener('DOMContentLoaded', function() {

    const passwordField = document.getElementById('password');
    const confirmationField = document.getElementById('confirmation');
    const registerForm = passwordField ? passwordField.form : null;

    if (passwordField && confirmationField && registerForm) {

        const messageElement = document.createElement('p');
        messageElement.style.color = 'red';
        confirmationField.parentNode.appendChild(messageElement);

        const checkPasswords = () => {
            const password = passwordField.value;
            const confirmation = confirmationField.value;

            if (confirmation.length > 0) {
                if (password === confirmation) {
                    messageElement.textContent = 'Passwords match!';
                    messageElement.style.color = 'green';
                } else {
                    messageElement.textContent = 'Passwords do not match!';
                    messageElement.style.color = 'red';
                }
            } else {
                messageElement.textContent = '';
            }
        };

        passwordField.addEventListener('keyup', checkPasswords);
        confirmationField.addEventListener('keyup', checkPasswords);
    }
});
