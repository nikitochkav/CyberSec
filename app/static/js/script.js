document.addEventListener('DOMContentLoaded', function() {
    // Код JavaScript для работы с DOM
    
    // Пример: Изменение стилей при наведении на ссылки в навигации
    const navLinks = document.querySelectorAll('nav ul li a');
    navLinks.forEach(link => {
        link.addEventListener('mouseover', function() {
            this.style.color = 'blue';
        });
        link.addEventListener('mouseout', function() {
            this.style.color = ''; // Сброс цвета при уходе мыши
        });
    });
    
    // Пример: Добавление анимации к заголовку
    const header = document.querySelector('header');
    const headerTitle = document.querySelector('.content h1');
if (headerTitle) {
    headerTitle.style.transition = 'transform 0.3s ease';
    header.addEventListener('mouseover', function() {
        headerTitle.style.transform = 'scale(1.1)';
    });
    header.addEventListener('mouseout', function() {
        headerTitle.style.transform = 'scale(1)';
    });
} else {
    console.error('Элемент h1 не найден внутри .content');
}
    
    // Добавление гифки
    const content = document.querySelector('.content');
    const gifImage = document.createElement('img'); 
    gifImage.src = 'static/images/fat_hacker.gif'; // Путь к вашей гифке
    gifImage.alt = 'Гифка'; 
    content.appendChild(gifImage);
    gifImage.classList.add('resized-gif'); // Добавляет класс к гифке
    
    // Другие интерактивные функции могут быть добавлены здесь
});
