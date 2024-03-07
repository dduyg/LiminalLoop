document.addEventListener('DOMContentLoaded', function () {
  const menuButton = document.getElementById('menuButton');
  const floatingMenu = document.getElementById('floatingMenu');

  menuButton.addEventListener('click', function () {
    floatingMenu.classList.toggle('hidden');
  });
});
