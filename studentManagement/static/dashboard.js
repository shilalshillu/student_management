function toggleSidebar() {
    const sidebar = document.querySelector('.sidebar');
    const toggleBtn = document.querySelector('.toggle-btn');

    sidebar.classList.toggle('collapsed');

    // Update the toggle button arrow direction
    if (sidebar.classList.contains('collapsed')) {
        toggleBtn.innerHTML = '⮞'; // Point right when closed
    } else {
        toggleBtn.innerHTML = '⮜'; // Point left when open
    }
}