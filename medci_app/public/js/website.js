// Setup SweetAlert Defaults
if (typeof Swal !== 'undefined') {
    const Toast = Swal.mixin({
        toast: true,
        position: 'top-end',
        showConfirmButton: false,
        timer: 3000,
        timerProgressBar: true
    });
    window.showToast = (icon, title) => Toast.fire({ icon, title });
} else {
    window.showToast = (icon, title) => alert(title);
}

// Button loading state manager
function setBtnLoading(btn, isLoading) {
    if (isLoading) {
        btn.classList.add('btn-loading');
        btn.disabled = true;
    } else {
        btn.classList.remove('btn-loading');
        btn.disabled = false;
    }
}
