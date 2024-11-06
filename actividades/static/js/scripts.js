document.addEventListener('DOMContentLoaded', function () {
    const sections = document.querySelectorAll('.section');
    const options = {
        threshold: 0.5
    };

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const leftElement = entry.target.querySelector('.animate-left');
                const rightElement = entry.target.querySelector('.animate-right');

                if (leftElement) {
                    leftElement.classList.add('in-view');
                }
                if (rightElement) {
                    rightElement.classList.add('in-view');
                }

                // Dejar de observar la sección una vez que se haya animado
                observer.unobserve(entry.target);
            }
        });
    }, options);

    sections.forEach(section => {
        observer.observe(section);
    });
});

