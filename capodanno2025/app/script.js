// Hero animations
gsap.fromTo(
    ".animated-title",
    { opacity: 0, y: 50 },
    { opacity: 1, y: 0, duration: 1.5, delay: 0.5 }
);

gsap.fromTo(
    ".animated-subtitle",
    { opacity: 0, y: 20 },
    { opacity: 1, y: 0, duration: 1.5, delay: 1 }
);

// Toggle the expanded details
document.getElementById("expand-details").addEventListener("click", function () {
    const details = document.getElementById("details-content");
    if (details.style.display === "none" || !details.style.display) {
        details.style.display = "block";
        this.textContent = "Nascondi Dettagli";
    } else {
        details.style.display = "none";
        this.textContent = "Mostra Dettagli";
    }
});


// Gallery animations on scroll
const images = document.querySelectorAll(".image-wrapper");
images.forEach((image, index) => {
    gsap.fromTo(
        image,
        { opacity: 0, x: 100 * (index % 2 === 0 ? 1 : -1) },
        {
            opacity: 1,
            x: 0,
            duration: 1,
            scrollTrigger: {
                trigger: image,
                start: "top 80%",
            },
        }
    );
});
