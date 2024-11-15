function toggleInputField() {
    const usernameDropdown = document.getElementById('username');
    const customInputWrapper = document.getElementById('customInputWrapper');

    if (usernameDropdown.value === 'Other') {
        customInputWrapper.style.display = 'block';
    } else {
        customInputWrapper.style.display = 'none';
    }
}