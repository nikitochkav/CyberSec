document.addEventListener('DOMContentLoaded', function () {
    // Изменение стилей при наведении на ссылки в навигации
    const navLinks = document.querySelectorAll('nav ul li a');
    navLinks.forEach(link => {
        link.addEventListener('mouseover', function () {
            this.style.color = 'gray';
        });
        link.addEventListener('mouseout', function () {
            this.style.color = '';
        });
    });

    // Добавление гифки
    const content = document.querySelector('.content');
    const gifImage = document.createElement('img');
    gifImage.src = 'static/images/fat_hacker.gif';
    gifImage.alt = 'Гифка';
    content.appendChild(gifImage);
    gifImage.classList.add('resized-gif');
});
