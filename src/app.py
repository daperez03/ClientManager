import gradio as gr


if __name__ == "__main__":
	with gr.Blocks() as app:
		pass

	app.launch(
		server_name="0.0.0.0",
		server_port=8080
    )
