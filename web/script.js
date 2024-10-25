// Seleziona l'elemento video
const video = document.getElementById('bg-video');

// Assicura che il video si riproduca automaticamente una volta caricato
video.addEventListener('loadeddata', () => {
    video.play();
});

// Impedisci il download del video tramite clic destro
video.addEventListener('contextmenu', function(e) {
    e.preventDefault(); // Blocca il menu contestuale sul video
});

// Funzione per il Countdown Moderno
function countdown() {
    const eventDate = new Date("November 23, 2024 15:00:00").getTime();
    const now = new Date().getTime();
    const timeLeft = eventDate - now;

    const days = Math.floor(timeLeft / (1000 * 60 * 60 * 24));
    const hours = Math.floor((timeLeft % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutes = Math.floor((timeLeft % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((timeLeft % (1000 * 60)) / 1000);

    document.getElementById("days").textContent = days < 10 ? "0" + days : days;
    document.getElementById("hours").textContent = hours < 10 ? "0" + hours : hours;
    document.getElementById("minutes").textContent = minutes < 10 ? "0" + minutes : minutes;
    document.getElementById("seconds").textContent = seconds < 10 ? "0" + seconds : seconds;

    if (timeLeft < 0) {
        clearInterval(countdownInterval);
        document.getElementById("countdown").innerHTML = "L'evento è iniziato!";
    }
}

// Aggiorna il countdown ogni secondo
const countdownInterval = setInterval(countdown, 1000);

// Effetto di transizione per la sezione descrizione
window.addEventListener('scroll', function() {
    const descriptionSection = document.querySelector('#description');
    const sectionPosition = descriptionSection.getBoundingClientRect().top;
    const screenPosition = window.innerHeight / 1.3;

    if (sectionPosition < screenPosition) {
        descriptionSection.style.opacity = '1';
        descriptionSection.style.transform = 'translateY(0)';
    }
});

// Effetto di transizione per la sezione descrizione
window.addEventListener('scroll', function() {
    const descriptionSection = document.querySelector('#description');
    const sectionPosition = descriptionSection.getBoundingClientRect().top;
    const screenPosition = window.innerHeight / 1.3;

    if (sectionPosition < screenPosition) {
        descriptionSection.style.opacity = '1';
        descriptionSection.style.transform = 'translateY(0)';
    }
});

// Seleziona gli elementi per i pulsanti e la descrizione dettagliata
const detailsBtn = document.getElementById('details-btn');
const eventDetails = document.getElementById('event-details');

// Aggiungi un evento di click per mostrare/nascondere la descrizione dettagliata
detailsBtn.addEventListener('click', function() {
    if (eventDetails.classList.contains('hidden')) {
        eventDetails.classList.remove('hidden');
        eventDetails.classList.add('visible');
        detailsBtn.textContent = 'Nascondi dettagli';
    } else {
        eventDetails.classList.remove('visible');
        eventDetails.classList.add('hidden');
        detailsBtn.textContent = 'Mostra dettagli';
    }
});

// Pulsanti placeholder per azioni specifiche (apertura mappa e iscrizione)
document.getElementById('location-btn').addEventListener('click', function() {
    alert("La mappa del luogo sarà disponibile presto.");
});

document.getElementById('register-btn').addEventListener('click', function() {
    alert("La registrazione sarà disponibile a breve.");
});
