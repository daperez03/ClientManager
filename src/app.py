import os

import gradio as gr
from sqlalchemy import create_engine, or_
from sqlalchemy.orm import sessionmaker

from models.Client import Client


DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///clients.db")
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


def create_schema():
    Client.__table__.metadata.create_all(engine)


def _normalize(value):
    if value is None:
        return ""
    return str(value).strip()


def _client_to_dict(client):
    return {
        "id": client.id,
        "name": client.name,
        "email": client.email,
        "phone": client.phone,
    }


def create_client(name: str, email: str, phone: str):
    """
    Creates a new client in the database.

    Args:
        name (str): The name of the client.
        email (str): The email of the client.
        phone (str): The phone number of the client.

    Returns:
        str: Message indicating the result of the operation.
    """
    name = _normalize(name)
    email = _normalize(email)
    phone = _normalize(phone)

    if not all((name, email, phone)):
        return "Complete todos los campos."

    if "@" not in email or "." not in email.split("@")[-1]:
        return "Correo electrónico inválido."

    try:
        with Session() as session:
            new_client = Client(name=name, email=email, phone=phone)
            session.add(new_client)
            session.commit()
        return "Cliente creado correctamente."
    except Exception as exc:
        return f"Error al crear el cliente: {exc}"


def read_clients(search: str = ""):
    """Returns a list of client dictionaries, optionally filtered by a search term."""
    search_term = _normalize(search)

    try:
        with Session() as session:
            query = session.query(Client)
            if search_term:
                like_term = f"%{search_term}%"
                query = query.filter(
                    or_(
                        Client.name.ilike(like_term),
                        Client.email.ilike(like_term),
                        Client.phone.ilike(like_term),
                    )
                )
            clients = query.order_by(Client.id).all()
            return [_client_to_dict(client) for client in clients]
    except Exception:
        return []


def update_client(client_id: int, name: str, email: str, phone: str):
    """
    Updates an existing client in the database.

    Args:
        client_id (int): The ID of the client to update.
        name (str): The new name of the client.
        email (str): The new email of the client.
        phone (str): The new phone number of the client.

    Returns:
        str: Message indicating the result of the operation.
    """
    name = _normalize(name)
    email = _normalize(email)
    phone = _normalize(phone)

    if not all((name, email, phone)):
        return "Complete todos los campos."

    if "@" not in email or "." not in email.split("@")[-1]:
        return "Correo electrónico inválido."

    try:
        with Session() as session:
            client = session.get(Client, client_id)

            if client is None:
                return "Cliente no encontrado."

            client.name = name
            client.email = email
            client.phone = phone

            session.commit()

        return "Cliente actualizado correctamente."

    except Exception as exc:
        return f"Error al actualizar el cliente: {exc}"


def delete_client(client_id: int, confirm: bool = True):
   pass

def read_clients_table(search: str = ""):
    clients = read_clients(search)
    return [[client["id"], client["name"], client["email"], client["phone"]] for client in clients]


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
            search = gr.Textbox(label="Buscar por nombre, correo o teléfono", placeholder="Escribe para filtrar los clientes")
            refresh_button = gr.Button("Buscar clientes", variant="secondary")
            table = gr.DataFrame(
                headers=["ID", "Nombre", "Correo", "Teléfono"],
                interactive=False,
                row_count=(5, "dynamic"),
            )
            refresh_button.click(read_clients_table, inputs=search, outputs=table)
            search.submit(read_clients_table, inputs=search, outputs=table)
            app.load(read_clients_table, inputs=search, outputs=table)

        with gr.Tab("Actualizar cliente"):
            update_id = gr.Number(label="ID del cliente", precision=0)
            update_name = gr.Textbox(label="Nuevo nombre")
            update_email = gr.Textbox(label="Nuevo correo electrónico", type="email")
            update_phone = gr.Textbox(label="Nuevo teléfono")
            update_button = gr.Button("Actualizar cliente", variant="primary")
            update_result = gr.Textbox(label="Resultado", interactive=False)
            update_button.click(
                update_client,
                inputs=[update_id, update_name, update_email, update_phone],
                outputs=update_result,
            )

        with gr.Tab("Eliminar cliente"):
            delete_id = gr.Number(label="ID del cliente", precision=0)
            confirm_delete = gr.Checkbox(label="Confirmar eliminación")
            delete_button = gr.Button("Eliminar cliente", variant="stop")
            delete_result = gr.Textbox(label="Resultado", interactive=False)
            delete_button.click(
                delete_client,
                inputs=[delete_id, confirm_delete],
                outputs=delete_result,
            )

    return app


if __name__ == "__main__":
    create_schema()
    build_app().launch(server_name="0.0.0.0", server_port=8080)
