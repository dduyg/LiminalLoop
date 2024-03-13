const menuBtn = document.querySelector('.logo');
const menu = document.querySelector('.menu');
const menuItems = document.querySelectorAll('.menu li a');

// Toggle menu active class
menuBtn.addEventListener('click', () => {
    menu.classList.toggle('active');
});

// Close menu when a menu item is clicked
menuItems.forEach(item => {
    item.addEventListener('click', () => {
        menu.classList.remove('active');
    });
});
