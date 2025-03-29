// Variable para almacenar la posición inicial del scroll
let ubicacioPrincipal = window.pageYOffset;

// Inicialización de la librería AOS (Animate On Scroll)
AOS.init();

// Evento para manejar el scroll y mostrar/ocultar el menú de navegación
window.addEventListener("scroll", function() {
    // Obtener la posición actual del scroll
    let desplazamientoActual = window.pageYOffset;
    
    // Mostrar u ocultar el menú según la dirección del scroll
    if (ubicacioPrincipal >= desplazamientoActual) {
        document.getElementsByTagName("nav")[0].style.top = "0px"; // Mostrar menú
    } else {
        document.getElementsByTagName("nav")[0].style.top = "-100px"; // Ocultar menú
    }
    
    // Actualizar la posición principal del scroll
    ubicacioPrincipal = desplazamientoActual;
});

// Variables para el menú hamburguesa
let enlacesHeader = document.querySelectorAll(".enlaces-header")[0];
let semaforo = true; // Controla el estado del menú (abierto/cerrado)

// Evento para abrir/cerrar el menú hamburguesa
document.querySelectorAll(".hamburguer")[0].addEventListener("click", function() {
    if (semaforo) {
        document.querySelectorAll(".hamburguer")[0].style.color = "#fff"; // Cambiar color del ícono
        semaforo = false; // Menú abierto
    } else {
        document.querySelectorAll(".hamburguer")[0].style.color = "#000"; // Cambiar color del ícono
        semaforo = true; // Menú cerrado
    }
    // Alternar la clase "menudos" para mostrar/ocultar el menú
    enlacesHeader.classList.toggle("menudos");
});

// Función para desplazarse a la sección de "Ruta de Aprendizaje"
function scrollToRutaAprendizaje() {
    const rutaAprendizaje = document.getElementById('ruta-aprendizaje');
    if (rutaAprendizaje) {
        rutaAprendizaje.scrollIntoView({ behavior: 'smooth' }); // Desplazamiento suave
    }
}

// Verificar si el hash en la URL es #ruta-aprendizaje al cargar la página
window.addEventListener('load', function() {
    if (window.location.hash === '#ruta-aprendizaje') {
        scrollToRutaAprendizaje(); // Desplazarse a la sección
    }
});

// Función para mostrar un mensaje flash
function mostrarMensajeFlash() {
    // Crear el elemento del mensaje
    const mensajeFlash = document.createElement('div');
    mensajeFlash.textContent = '¡Inscripción exitosa!';
    mensajeFlash.style.position = 'fixed';
    mensajeFlash.style.bottom = '20px';
    mensajeFlash.style.right = '20px';
    mensajeFlash.style.backgroundColor = '#4CAF50';
    mensajeFlash.style.color = 'white';
    mensajeFlash.style.padding = '15px';
    mensajeFlash.style.borderRadius = '5px';
    mensajeFlash.style.zIndex = '1000';
    mensajeFlash.style.boxShadow = '0 4px 8px rgba(0, 0, 0, 0.2)';
    mensajeFlash.style.animation = 'fadeInOut 3s ease-in-out';

    // Agregar el mensaje al cuerpo del documento
    document.body.appendChild(mensajeFlash);

    // Eliminar el mensaje después de 3 segundos
    setTimeout(() => {
        document.body.removeChild(mensajeFlash);
    }, 3000);
}

// Función para verificar el estado de sesión y actualizar la navegación
function verificarSesion() {
    fetch('/check_session')
        .then(response => response.json())
        .then(data => {
            const loginLink = document.getElementById('loginLink');
            const registroLink = document.getElementById('registroLink');
            const misCursosLink = document.getElementById('misCursosLink');
            const logoutLink = document.getElementById('logoutLink');
            const adminLink = document.getElementById('adminLink');

            // Mostrar u ocultar enlaces según el estado de sesión
            if (data.logueado) {
                if (loginLink) loginLink.style.display = 'none';
                if (registroLink) registroLink.style.display = 'none';
                if (misCursosLink) misCursosLink.style.display = 'block';
                if (logoutLink) logoutLink.style.display = 'block';
                if (adminLink && data.es_admin) adminLink.style.display = 'block';
            } else {
                if (loginLink) loginLink.style.display = 'block';
                if (registroLink) registroLink.style.display = 'block';
                if (misCursosLink) misCursosLink.style.display = 'none';
                if (logoutLink) logoutLink.style.display = 'none';
                if (adminLink) adminLink.style.display = 'none';
            }
        });
}

// Verificar sesión al cargar la página
window.addEventListener('load', verificarSesion);

// Función para inscribirse en un curso
function inscribirseEnCurso(cursoNombre) {
    // Obtener el ID del curso basado en su nombre
    fetch('/obtener_curso_id', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ nombre: cursoNombre })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error); // Mostrar mensaje de error
            return;
        }
        const cursoId = data.curso_id;

        // Inscribirse en el curso
        fetch('/inscribirse', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ curso_id: cursoId })
        })
        .then(response => {
            if (response.status === 401) {
                return response.json().then(data => {
                    alert(data.mensaje); // Mostrar mensaje de error
                    window.location.href = data.redirect; // Redirigir al usuario
                });
            }
            return response.json();
        })
        .then(data => {
            mostrarMensajeFlash(); // Mostrar mensaje de éxito
            verificarSesion(); // Actualizar la navegación
            mostrarCursosInscritos(); // Actualizar la lista de cursos
        })
        .catch(error => console.error('Error:', error));
    })
    .catch(error => console.error('Error:', error));
}
