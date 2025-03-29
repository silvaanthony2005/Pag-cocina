# Proyecto de Cursos de Cocina

Este proyecto es una plataforma web para la gestión de cursos de cocina, que incluye funcionalidades de registro, login, gestión de usuarios, inscripción a cursos, y un chatbot integrado con Botpress.

## Tecnologías Utilizadas

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python (Flask)
- **Base de Datos**: SQLite
- **Chatbot**: Botpress
- **Animaciones**: AOS (Animate On Scroll)
- **Iconos**: Font Awesome
- **Mapas**: OpenStreetMap

## Estructura del Proyecto

### Archivos Principales

- `app.py`: Contiene la lógica del servidor Flask y las rutas principales.
- `models.py`: Define los modelos de la base de datos.
- `templates/`: Contiene las plantillas HTML.
- `static/`: Contiene archivos estáticos (CSS, JS, imágenes).

### Funcionalidades

#### Registro y Login

- **Registro**: Los usuarios pueden registrarse proporcionando su nombre, correo electrónico y contraseña. La contraseña se almacena de forma segura utilizando hashing.
- **Login**: Los usuarios pueden iniciar sesión con su correo electrónico y contraseña. La sesión se mantiene activa utilizando cookies. 

#### Gestión de Usuarios

- **Edición de Usuarios**: Los administradores pueden editar la información de los usuarios, incluyendo su rol (admin o no admin).
- **Eliminación de Usuarios**: Los administradores pueden eliminar usuarios del sistema.

#### Cursos e Inscripción

- **Listado de Cursos**: Los usuarios pueden ver los cursos disponibles y su progreso en cada uno.
- **Inscripción**: Los usuarios pueden inscribirse en cursos, lo que se refleja en su perfil.

#### Chatbot con Botpress

- **Integración**: El chatbot se integra en todas las páginas mediante un botón flotante. Se inicializa con un script de Botpress y se muestra/oculta al hacer clic en el botón.
- **Personalización**: El chatbot utiliza los colores de la página y un ícono personalizado.

### Base de Datos

La base de datos se maneja con SQLite y se define en `models.py`. Incluye tablas para usuarios, cursos, y la relación entre usuarios y cursos.

### Rutas en `app.py`

- **`/`**: Página principal con información sobre los cursos.
- **`/login`**: Página de inicio de sesión.
- **`/registro`**: Página de registro de nuevos usuarios.
- **`/mis_cursos`**: Página que muestra los cursos en los que el usuario está inscrito.
- **`/gestion_usuarios`**: Página de gestión de usuarios (solo para administradores).
- **`/editar_usuario/<usuario_id>`**: Página para editar la información de un usuario.

### Integración del Chatbot

El chatbot se integra en todas las páginas mediante un script de Botpress. Se inicializa con un botón flotante que muestra/oculta el chat al hacer clic.

### Animaciones y Estilos

Se utilizan animaciones de AOS (Animate On Scroll) para mejorar la experiencia del usuario. Los estilos se definen en `static/css/estilos.css` y `static/css/botpress.css`.

### Cómo Ejecutar el Proyecto

1. Instala las dependencias: `pip install -r requirements.txt`.
2. Ejecuta el servidor: `python app.py`.
3. Accede a la aplicación en `http://localhost:5000`.

### Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o envía un pull request con tus mejoras.

### Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo `LICENSE` para más detalles.
