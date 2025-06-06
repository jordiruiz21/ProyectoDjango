window.addEventListener('DOMContentLoaded', () => {
    const container = document.getElementById('svgCuerpoContainer');

    fetch("/static/models/cuerpo_humano4.svg")
        .then(res => res.text())
        .then(svgText => {
            container.innerHTML = svgText;
            const svgDoc = container.querySelector('svg');

            const videosPorMusculo = {
                biceps: ['https://www.youtube.com/embed/ykJmrZ5v0Oo', 'https://www.youtube.com/embed/6zIuAyLZPH0', 'https://www.youtube.com/embed/1Tq3QdYUuHs'],
                triceps: ['https://www.youtube.com/embed/6SSWbAfJ9ME', 'https://www.youtube.com/embed/2-LAMcpzODU'],
                pecho: ['https://www.youtube.com/embed/eozdVDA78K0', 'https://www.youtube.com/embed/SQHf9gqV5E4'],
                cuadriceps: ['https://www.youtube.com/embed/s6zR2T9vn2c', 'https://www.youtube.com/embed/tEoSTa1b90E'],
                hombro: ['https://www.youtube.com/embed/2yjwXTZQDDI', 'https://www.youtube.com/embed/0JfYxMRsUCQ'],
                gemelo: ['https://www.youtube.com/embed/-M4-G8p8fmc', 'https://www.youtube.com/embed/IUZJoSP66HI'],
                abdomen: ['https://www.youtube.com/embed/1919eTCoESo', 'https://www.youtube.com/embed/AnYl6Nk9GOA'],
                dorsal: ['https://www.youtube.com/embed/2LiDCgXf5aA', 'https://www.youtube.com/embed/pmyNz2xPU4Y'],
                gluteos: ['https://www.youtube.com/embed/2-D4V2On_eQ', 'https://www.youtube.com/embed/Rr6eGfWFE5k'],
                trapecios: ['https://www.youtube.com/embed/XKt1yptMMGc'],
                femoral: ['https://www.youtube.com/embed/5i5AqBjM1BU'],
                aductor: ['https://www.youtube.com/embed/IhA8kZjLt0s']
            };

            const alias = {
                'biceps-2': 'biceps', 'triceps-2': 'triceps', 'cuadriceps-2': 'cuadriceps',
                'hombro-2': 'hombro', 'gemelo-2': 'gemelo', 'dorsal-2': 'dorsal',
                'gluteos-2': 'gluteos', 'femoral-2': 'femoral', 'aductor-2': 'aductor'
            };

            const musculos = [
                'biceps', 'biceps-2', 'pecho',
                'cuadriceps', 'cuadriceps-2',
                'hombro', 'hombro-2',
                'triceps', 'triceps-2',
                'gemelo', 'gemelo-2',
                'abdomen',
                'dorsal', 'dorsal-2',
                'gluteos', 'gluteos-2',
                'trapecios',
                'femoral', 'femoral-2',
                'aductor', 'aductor-2'
            ];

            musculos.forEach(id => {
                const zona = svgDoc.getElementById(id);
                if (zona) {
                    zona.style.cursor = 'pointer';
                    zona.style.fill = 'rgba(255, 255, 255, 0.01)';

                    zona.addEventListener('mouseover', () => {
                        zona.style.fill = 'rgba(255, 0, 0, 0.5)';
                    });

                    zona.addEventListener('mouseout', () => {
                        zona.style.fill = 'rgba(255, 255, 255, 0.01)';
                    });

                    zona.addEventListener('click', () => {
                        const key = alias[id] || id;
                        const videos = videosPorMusculo[key];
                        const videoContainer = document.getElementById('videoContainer');

                        if (videos?.length) {
                            videoContainer.innerHTML = videos.map(url => `
                                <div class="col-sm-6 col-md-6 col-lg-6">
                                    <div class="ratio ratio-16x9">
                                        <iframe src="${url}" frameborder="0" allowfullscreen></iframe>
                                    </div>
                                </div>
                            `).join('');
                            videoContainer.classList.add('highlight-video');
                            setTimeout(() => videoContainer.classList.remove('highlight-video'), 2000);

                            const offset = videoContainer.getBoundingClientRect().top + window.scrollY - (window.innerHeight / 2) + (videoContainer.offsetHeight / 2);
                            window.scrollTo({ top: offset, behavior: 'smooth' });
                        }
                    });
                }
            });
        })
        .catch(err => {
            console.error('Error cargando SVG:', err);
            container.innerHTML = '<p>Error al cargar el SVG.</p>';
        });
});
