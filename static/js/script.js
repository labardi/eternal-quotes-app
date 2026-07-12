async function getNextQuote(event) {
    event.preventDefault();
    console.log("Отправляем запрос на сервер...")

    try {
        const quoteText = document.querySelector('.quote-text');
        const quoteAuthor = document.querySelector('.quote-author');

        quoteText.classList.remove('fade-in-text');
        quoteAuthor.classList.remove('fade-in-text');

        const response = await fetch('/api/next_quote');
        const data = await response.json();

        const visibleImage = document.querySelector('.bg-layer.active')
        const hiddenImage = document.querySelector('.bg-layer:not(.active)');

        if (data['time_to_swap'] === true) {
            const applySwap = function() {
                hiddenImage.classList.add('active');
                visibleImage.classList.remove('active');
             }

            hiddenImage.onload = applySwap;

            hiddenImage.srcset = data["str_next_urls"];
            hiddenImage.sizes = "100vw";

            if (hiddenImage.complete) { applySwap(); }

        } else {

            hiddenImage.onload = null;
            hiddenImage.srcset = data["str_next_urls"];

        }

        quoteText.textContent = data['quote']['text'];
        quoteAuthor.textContent = data['quote']['author'];

        void quoteText.offsetWidth;

        quoteText.classList.add('fade-in-text');
        quoteAuthor.classList.add('fade-in-text');


    } catch (error) {
        console.error("Ошибка при запросе: ", error);
    }
}

const nextQuoteButton = document.querySelector('.icon-button');

nextQuoteButton.addEventListener('click', getNextQuote);