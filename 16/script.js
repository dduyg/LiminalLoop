document.addEventListener('DOMContentLoaded', function () {
  const menuToggle = document.getElementById('menu-toggle');
  const menu = document.querySelector('nav ul');

  menuToggle.addEventListener('click', function () {
    menu.classList.toggle('active');
  });
});
