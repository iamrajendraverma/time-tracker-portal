document.addEventListener('DOMContentLoaded', () => {
    // Auto-hide flash messages after 5 seconds
    const flashMessages = document.querySelectorAll('.flash-msg');
    flashMessages.forEach(msg => {
        setTimeout(() => {
            msg.style.opacity = '0';
            setTimeout(() => msg.remove(), 300); // Wait for transition
        }, 5000);
    });
});
