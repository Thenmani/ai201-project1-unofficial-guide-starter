import gradio as gr
from query import ask

sample_questions = [
    "Select a sample question...",
    "Is COP 4710 (Database Management) a difficult course?",
    "What do students say about the exams in CHM 1045 (General Chemistry I)?",
    "What do students say about online courses at FIU?",
    "What are the hardest CS courses at FIU according to students?",
    "How much programming experience is needed before taking COP 3530 (Data Structures)?",
]

def handle_query(question):
    if not question.strip() or question == "Select a sample question...":
        return "Please enter or select a question first.", ""
    result = ask(question)
    sources = "\n".join(f"- {s}" for s in result["sources"])
    return result["answer"], sources

def load_question(selected):
    if selected == "Select a sample question...":
        return ""
    return selected

with gr.Blocks(title="FIU Unofficial Course Guide") as demo:

    gr.Markdown("# FIU Unofficial Course Review Guide")
    gr.Markdown("### Your AI-powered guide to real student experiences at Florida International University")
    gr.Markdown("---")
    gr.Markdown("> How it works: Select a sample question or type your own. Answers are grounded in real student reviews from Reddit, PantherNOW, and Professors Directory.")

    dropdown = gr.Dropdown(
        choices=sample_questions,
        value="Select a sample question...",
        label="Select Question",
        interactive=True
    )

    inp = gr.Textbox(
        label="Your Question",
        placeholder="e.g. What do students say about online courses at FIU?",
        lines=2
    )

    btn = gr.Button("Ask", variant="primary", size="lg")

    gr.Markdown("---")

    with gr.Row():
        with gr.Column(scale=2):
            answer = gr.Textbox(
                label="Answer",
                lines=10
            )
        with gr.Column(scale=1):
            sources = gr.Textbox(
                label="Retrieved From",
                lines=10,
                interactive=False
            )

    gr.Markdown("---")
    gr.Markdown("> Disclaimer: Answers are based on student-generated content and may not reflect official FIU policies. Always verify with your academic advisor.")

    dropdown.change(load_question, inputs=dropdown, outputs=inp)
    btn.click(handle_query, inputs=inp, outputs=[answer, sources])
    inp.submit(handle_query, inputs=inp, outputs=[answer, sources])

demo.launch()