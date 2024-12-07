// Funzione per aggiornare il countdown
function updateCountdown() {
    const targetDate = new Date('January 1, 2025 00:00:00').getTime(); // Data di riferimento
    const now = new Date().getTime(); // Data corrente
    const timeLeft = targetDate - now; // Differenza tra le date

    if (timeLeft >= 0) {
        const days = Math.floor(timeLeft / (1000 * 60 * 60 * 24));
        const hours = Math.floor((timeLeft % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((timeLeft % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((timeLeft % (1000 * 60)) / 1000);

        // Aggiorna il DOM con i valori
        document.getElementById('days').textContent = days;
        document.getElementById('hours').textContent = hours;
        document.getElementById('minutes').textContent = minutes;
        document.getElementById('seconds').textContent = seconds;
    } else {
        // Mostra un messaggio quando il countdown è terminato
        document.getElementById('countdown').innerHTML = "<h3>Buon Anno Nuovo!</h3>";
    }
}

// Aggiorna il countdown ogni secondo
setInterval(updateCountdown, 1000);

// Animazioni per la hero section (GSAP)
gsap.fromTo(
    ".animated-title",
    { opacity: 0, y: 50 },
    { opacity: 1, y: 0, duration: 1.5, delay: 0.5 }
);

gsap.fromTo(
    ".logo",
    { opacity: 0, scale: 0.5 },
    { opacity: 1, scale: 1, duration: 1.5, delay: 0.3 }
);

// Mostra/nasconde i dettagli nella sezione "Eventi"
document.getElementById('details-btn').addEventListener('click', function () {
    const eventDetails = document.getElementById('details-content');
    if (eventDetails.classList.contains('hidden')) {
        eventDetails.classList.remove('hidden'); // Mostra i dettagli
        this.textContent = 'Nascondi dettagli';
    } else {
        eventDetails.classList.add('hidden'); // Nasconde i dettagli
        this.textContent = 'Mostra dettagli';
    }
});


// Pulsante "Vedi il luogo"
document.getElementById('location-btn').addEventListener('click', function () {
    window.location.href = 'https://maps.app.goo.gl/xs178HzJaQ5HbLrb8'; // Reindirizzamento al link specificato
});

// Pulsante "Iscriviti ora"
document.getElementById('register-btn').addEventListener('click', function () {
    window.location.href = 'https://forms.gle/GHjFbTCCp6t7D77z9'; // Reindirizzamento al link specificato
});

