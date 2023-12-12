/**
 * Обработчик события DOMContentLoaded.
 * Обеспечивает функциональность согласия на использование куки.
 */
document.addEventListener('DOMContentLoaded', function () {
    const cookieConsent = document.querySelector('.cookie-consent');

    if (cookieConsent) {
        const acceptButton = cookieConsent.querySelector('button');
        const declineLink = cookieConsent.querySelector('a');

        // Проверяем наличие cookie_consent в куках
        const consentCookie = document.cookie.split(';').find(cookie => cookie.trim().startsWith('cookie_consent='));
        if (!consentCookie) {
            cookieConsent.style.display = 'block';
        }

        // Обработчик согласия
        acceptButton.addEventListener('click', function () {
            document.cookie = 'cookie_consent=true; max-age=' + (365 * 24 * 60 * 60);
            cookieConsent.style.display = 'none';
        });

        // Обработчик отказа
        declineLink.addEventListener('click', function () {
            cookieConsent.style.display = 'none';
        });
    }
});
