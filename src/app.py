import os

import gradio as gr
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from models.Client import Client


DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

def create_schema():
    Client.__table__.metadata.create_all(engine)


def create_client(name: str, email: str, phone: str):
    """
    Creates a new client in the database.

    Args:
        name (str): The name of the client.
        email (str): The email of the client.
        phone (str): The phone number of the client.

    Returns:
        Client: The created client object.
    """
    if not all(value and value.strip() for value in (name, email, phone)):
        return "Complete todos los campos."
    try:
        with Session(engine) as session:
            new_client = Client(name=name.strip(), email=email.strip(), phone=phone.strip())
            session.add(new_client)
            session.commit()
        return "Cliente creado correctamente."
    except Exception as e:
        return f"Error al crear el cliente: {str(e)}"

def read_clients():
    pass

def update_client(client_id: int, name: str, email: str, phone: str):
    pass

def delete_client(client_id: int):
    pass


def build_app():
    with gr.Blocks(theme=gr.themes.Soft(primary_hue="sky")) as app:
        gr.Markdown("# Gestión de clientes")

        with gr.Tab("Crear cliente"):
            name = gr.Textbox(label="Nombre")
            email = gr.Textbox(label="Correo electrónico", type="email")
            phone = gr.Textbox(label="Teléfono")
            create_button = gr.Button("Crear cliente", variant="primary")
            result = gr.Textbox(label="Resultado", interactive=False)
            create_button.click(
                create_client,
                inputs=[name, email, phone],
                outputs=result,
            )

        with gr.Tab("Consultar clientes"):
            gr.Markdown("Próximamente: consultar y listar clientes.")

        with gr.Tab("Actualizar cliente"):
            gr.Markdown("Próximamente: actualizar clientes.")

        with gr.Tab("Eliminar cliente"):
            gr.Markdown("Próximamente: eliminar clientes.")

    return app

if __name__ == "__main__":
    create_schema()
    build_app().launch(server_name="0.0.0.0", server_port=8080)
