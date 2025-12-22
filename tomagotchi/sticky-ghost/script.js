// JavaScript is used to add a class when the user scrolls down, making the header sticky

const header = document.querySelector('.sticky-header');

window.addEventListener('scroll', () => {
  if (window.scrollY > 0) {
    header.classList.add('sticky');
  } else {
    header.classList.remove('sticky');
  }
});
