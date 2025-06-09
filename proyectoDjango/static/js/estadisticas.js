const datos = JSON.parse(document.getElementById('datos-entrenamiento').textContent);

    const ejercicioSelect = document.getElementById('ejercicioSelect');
    const ctx = document.getElementById('pesoChart').getContext('2d');
    const btnPeso = document.getElementById('btnPeso');
    const btnTotal = document.getElementById('btnTotal');

    const ejercicios = Object.keys(datos);
    ejercicios.forEach(ej => {
        const option = document.createElement('option');
        option.value = ej;
        option.textContent = ej;
        ejercicioSelect.appendChild(option);
    });

    let chart;
    let modo = 'peso'; // por defecto
    

    function crearGrafico(ejercicio) {
        let yLabel = modo === 'peso' ? 'Kilos Levantados (media)' : 'Peso Total (media peso × repes)';
        let yStep = modo === 'peso' ? 2 : 20;
        const registros = datos[ejercicio];
        const fechas = registros.map(r => r.fecha);
        const pesos = registros.map(r => r.peso);
        const totales = registros.map(r => r.total);

        if (chart) chart.destroy();

        let datasets = [];

        if (modo === 'peso') {
            datasets = [{
                label: 'Peso Medio',
                data: pesos,
                borderColor: 'rgba(54, 162, 235, 1)', // azul claro
                backgroundColor: 'rgba(54, 162, 235, 0.2)', // relleno azul claro
                tension: 0.3, // suaviza la línea
                borderWidth: 2,
                pointRadius: 5,
                pointBackgroundColor: 'blue',
                fill: true,
            }];
        } else {
            datasets = [{
                label: 'Peso Total (peso x repes)',
                data: totales,
                borderColor: 'rgb(75, 192, 134)',
                backgroundColor: 'rgba(75, 192, 128, 0.2)',
                tension: 0.3,
                borderWidth: 2,
                pointRadius: 5,
                pointBackgroundColor: 'green',
                fill: true,
            }];
        }

        chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: fechas,
                datasets: datasets
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: `Estadísticas de ${ejercicio}`,
                        font: {
                            size: 20,
                            family: 'Arial',
                            weight: 'bold',
                        },
                        color: '#ffffff',
                        padding: {
                            top: 10,
                            bottom: 30
                        }
                    },
                    legend: {
                        labels: {
                            font: {
                                size: 14,
                                style: 'italic',
                            },
                            color: '#ffffff'
                        }
                    },
                    tooltip: {
                        enabled: true,
                        callbacks: {
                            label: function(context) {
                                return `${context.dataset.label}: ${context.parsed.y}`;
                            }
                        }
                    }
                },
                scales: {
                    x: {
                         grid: {
                            display: true,
                            color: '#ffffff' // gris claro, cambia si no se ve bien con tu fondo
                        },
                        ticks: {
                            font: {
                                size: 12,
                                weight: 'bold'
                            },
                            color: '#ffffff'
                        },
                        title: {
                            display: true,
                            text: 'Fecha',
                            font: {
                                size: 14,
                                weight: 'bold'
                            }
                        }
                    },
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: yLabel,
                            font: {
                                size: 14,
                                weight: 'bold'
                            }
                        },
                        grid: {
                            display: true,
                            color: '#ffffff' // gris claro, cambia si no se ve bien con tu fondo
                        },
                        ticks: {
                            stepSize: yStep,
                            color: '#ffffff'
                        }
                    }
                }

            }
        });
    }

    ejercicioSelect.addEventListener('change', () => {
        crearGrafico(ejercicioSelect.value);
    });

    btnPeso.addEventListener('click', () => {
        modo = 'peso';
        btnPeso.classList.add('active');
        btnTotal.classList.remove('active');
        crearGrafico(ejercicioSelect.value);
    });

    btnTotal.addEventListener('click', () => {
        modo = 'total';
        btnTotal.classList.add('active');
        btnPeso.classList.remove('active');
        crearGrafico(ejercicioSelect.value);
    });

    if (ejercicios.length > 0) {
        ejercicioSelect.value = ejercicios[0];
        crearGrafico(ejercicios[0]);
    }

    