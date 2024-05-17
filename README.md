
# Paper Reviews Web Application, Review-INDEX

## Descripción

Esta es una aplicación web para compartir y hacer reseñas de artículos científicos. La aplicación está construida utilizando Flask para el backend, Jinja2 para las plantillas HTML y Sirope/REDIS para el almacenamiento.

## Requisitos

- Python 3.10+
- Redis
- Virtualenv (opcional, pero recomendado)

## Instalación

### Clonar el Repositorio

```sh
git clone https://github.com/rubenfb23/r-index
cd src
```

### Crear y Activar un Entorno Virtual

#### En Windows

```sh
python -m venv venv
venv\Scripts\activate
```

#### En MacOS/Linux

```sh
python -m venv venv
source venv/bin/activate
```

### Instalar Dependencias

```sh
pip install -r requirements.txt
```

### Configurar Redis

Asegúrate de que Redis está instalado y en ejecución en tu máquina. Puedes iniciar el servidor Redis con los siguientes comandos:

#### En Ubuntu/Debian

```sh
sudo service redis-server start
```

#### En RedHat/Fedora

```sh
sudo systemctl start redis
```

#### En MacOS (usando Homebrew)

```sh
brew services start redis
```

## Lanzar la Aplicación

### Ejecutar la Aplicación Flask

```sh
python run.py
```

La aplicación estará disponible en `http://127.0.0.1:5000`.

## Pruebas

### Ejecutar Pruebas Unitarias

```sh
python test_app.py
```

## Estructura del Proyecto

```
/nombre_del_proyecto
  /app
    /templates
      base.html
      index.html
      login.html
      register.html
      papers.html
      paper_detail.html
      add_paper.html
      add_post.html
      edit_paper.html
      edit_post.html
    /static
      /css
        styles.css
    /models
      __init__.py
      models.py
  /venv
  run.py
  test_app.py
  requirements.txt
  README.md
```

## Dependencias

Asegúrate de que las siguientes dependencias están listadas en `requirements.txt`:

```
Flask
Flask-Login
sirope
redis
unittest
```

## Uso

1. **Registro**: Crea una cuenta en la página de registro.
2. **Inicio de Sesión**: Inicia sesión con tus credenciales.
3. **Agregar Paper**: Agrega un nuevo artículo científico.
4. **Ver Papers**: Navega por los artículos científicos y sus reseñas.
5. **Agregar Reseña**: Agrega una reseña a un artículo científico.

## Contribuir

1. Realiza un fork del repositorio.
2. Crea una nueva rama (`git checkout -b feature/nueva-funcionalidad`).
3. Realiza tus cambios y haz un commit (`git commit -m 'Agregar nueva funcionalidad'`).
4. Envía tus cambios a la rama (`git push origin feature/nueva-funcionalidad`).
5. Abre un Pull Request.

## Licencia

Este proyecto está licenciado bajo los términos de la licencia MIT. Para más detalles, consulta el archivo `LICENSE`.