# ClientManager

Aplicación para la gestión de clientes, desarrollada con Python, Gradio y
SQLAlchemy.

## Aplicación desplegada

La aplicación se encuentra disponible en:

**[https://clientmanager-77c2.onrender.com/](https://clientmanager-77c2.onrender.com/)**

Este es un proyecto **100% CI/CD**. No es necesario levantar la aplicación
manualmente después de realizar cambios: una vez que el código llega a
`main`, el pipeline valida las pruebas y Render realiza automáticamente el
despliegue de la versión aprobada.

El despliegue únicamente se ejecuta cuando:

1. El código se integra en `main` mediante un Pull Request.
2. Las pruebas automatizadas terminan correctamente.
3. El Pull Request cuenta con la aprobación de al menos un colaborador.

Si alguna validación falla, el cambio no debe integrarse y la versión
publicada no se actualiza.

## Flujo de trabajo CI/CD

El repositorio cuenta con las siguientes validaciones:

- GitHub Actions instala las dependencias y ejecuta `pytest` en cada Pull
  Request dirigido a `main`.
- Las mismas pruebas se ejecutan nuevamente cuando un cambio llega a `main`.
- Render monitorea la rama `main` y despliega automáticamente los cambios
  aprobados.
- El proyecto utiliza Release Please para gestionar las versiones a partir
  de los cambios integrados en `main`.

### Reglas de protección de `main`

La rama `main` está protegida. No se permiten commits directos; todos los
cambios deben ingresar mediante un Pull Request que cumpla con:

- La aprobación de al menos un colaborador.
- La ejecución exitosa de las pruebas automatizadas.

Por lo tanto, el flujo normal para contribuir es:

```text
Crear rama → Realizar cambios → Abrir Pull Request → Pasar pruebas
→ Obtener una aprobación → Integrar en main → Despliegue automático
```

## Ejecución local

Aunque el despliegue es automático, el proyecto puede ejecutarse localmente
para desarrollar y validar cambios.

### Requisitos

- Python 3.12 o superior
- Una base de datos compatible con SQLAlchemy

### Instalación

Desde la raíz del proyecto:

```bash
python -m venv .venv
```

En Windows:

```powershell
.venv\Scripts\Activate.ps1
```

En macOS/Linux:

```bash
source .venv/bin/activate
```

Instalar las dependencias:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install pytest
```

Definir la variable de conexión a la base de datos antes de iniciar la
aplicación:

```powershell
$env:DATABASE_URL = "postgresql+psycopg://usuario:contraseña@host:5432/base_de_datos"
```

Luego ejecutar:

```bash
python src/app.py
```

La aplicación estará disponible en `http://localhost:8080`.

### Ejecutar las pruebas

```bash
python -m pytest -v
```

## Estructura principal

```text
ClientManager/
├── .github/workflows/       # Automatizaciones de CI/CD
├── src/
│   ├── app.py               # Aplicación Gradio y operaciones de clientes
│   └── models/Client.py     # Modelo de datos Client
├── tests/                   # Pruebas automatizadas
├── pytest.ini               # Configuración de pytest
└── requirements.txt         # Dependencias de Python
```

## Estado actual

La creación de clientes está implementada. Las funciones de consulta,
actualización y eliminación se encuentran preparadas para desarrollarse en
iteraciones posteriores.
