import gradio as gr
from crypt_utils import Crypto
from web import get_person_summary
from fpdf import FPDF
import os
import tempfile
crypto = Crypto()

def generate_summary(name, org, org_type):
    summary = get_person_summary(name, org, org_type)
    formatted = f"""
    <div style='background-color:#1f1f1f; color:white; padding:1em; border-radius:10px; white-space:pre-wrap; word-wrap:break-word;'>
        {summary}
    </div>
    """
    return formatted, summary

def export_summary(summary, file_type):
    suffix = f".{file_type}"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        filename = tmp.name
        if file_type == "pdf":
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            for line in summary.strip().split('\n'):
                pdf.cell(200, 10, txt=line, ln=1)
            pdf.output(filename)
        else:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(summary)
    return filename

def export_and_encrypt(summary, file_type):
    file_path = export_summary(summary, file_type)
    enc_path = crypto.encrypt_file(file_path)
    return enc_path

def decrypt_and_display(enc_file):
    return crypto.decrypt_file(enc_file)

with gr.Blocks() as demo:
    gr.Markdown("## 🔐 Professional Summary Generator", elem_id="title")

    with gr.Row():
        name = gr.Textbox(label="Name")
        org = gr.Textbox(label="Organization")
        org_type = gr.Textbox(label="Type of Organization")

    generate_btn = gr.Button("Generate Summary")
    summary_display = gr.HTML()
    hidden_summary = gr.Textbox(visible=False)

    with gr.Row():
        file_type = gr.Radio(["pdf", "txt"], label="Export Format", value="pdf")
        export_btn = gr.Button("Export & Download")
        encrypt_btn = gr.Button("Export & Encrypt")

    file_output = gr.File()

    decrypt_file_input = gr.File(label="Upload Encrypted File")
    decrypt_btn = gr.Button("Decrypt & Show Summary")
    decrypted_output = gr.Textbox(label="Decrypted Summary", lines=10)

    generate_btn.click(generate_summary, inputs=[name, org, org_type], outputs=[summary_display, hidden_summary])
    export_btn.click(export_summary, inputs=[hidden_summary, file_type], outputs=file_output)
    encrypt_btn.click(export_and_encrypt, inputs=[hidden_summary, file_type], outputs=file_output)
    decrypt_btn.click(decrypt_and_display, inputs=[decrypt_file_input], outputs=decrypted_output)

demo.launch(share=True)
