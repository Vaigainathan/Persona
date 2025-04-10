import gradio as gr

# Subcategories mapping
subcategory_options = {
    "Politics": ["Party1", "Party2", "Party3"],
    "Startup": ["Startup1", "Startup2"],
    "Celebrity": ["Kollywood", "Hollywood", "Tollywood","Bollywood"]
}

# Flatten all subcategory choices initially
all_subcategories = [item for sublist in subcategory_options.values() for item in sublist]

# Update subcategory options when category changes
def update_subcategories(category):
    return gr.update(choices=subcategory_options.get(category, []), visible=True)

# Handle form submission
def handle_submit(name, category, subcategory):
    return f"👤 Name  : {name}\n📂Category  : {category}\n📁Subcategory  : {subcategory}"

with gr.Blocks() as demo:
    gr.Markdown("## 📝 **Persona**")
    gr.Markdown("Fill out the form below to retrieve required details.")

    with gr.Row():
        with gr.Column():
            name_input = gr.Textbox(label="👤 Enter Your Name", placeholder="Type your name here...")
            category_dropdown = gr.Dropdown(
                label="📂 Select a Category", 
                choices=["Politics", "Startup", "Celebrity"], 
                interactive=True
            )
            subcategory_dropdown = gr.Dropdown(
                label="📁 Select a Subcategory", 
                choices=all_subcategories, 
                visible=True
            )

    # Update subcategory dropdown on category change
    category_dropdown.change(fn=update_subcategories, inputs=category_dropdown, outputs=subcategory_dropdown)

    submit_btn = gr.Button("🚀 Submit")
    output = gr.Textbox(label="📜 Result", lines=5, interactive=False)

    submit_btn.click(fn=handle_submit, inputs=[name_input, category_dropdown, subcategory_dropdown], outputs=output)

# Launch the app
demo.launch(share=True)
