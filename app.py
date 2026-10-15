import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

# Load keys from the project's .env file.
load_dotenv(Path(__file__).resolve().parent / ".env")

from project import build_pipeline  # noqa: E402


st.set_page_config(
    page_title="Script Studio | AI Workflow",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

EXAMPLE_TEXT = (
    "Narrator: The old clockmaker fixed the golden watch, and time suddenly froze "
    "for everyone else. Leo: (Gasping) Why is the rain stopping in mid-air? "
    "Narrator: He realized he now held the power to change history."
)

# Visual styling
st.markdown(
    """
    <style>
      .stApp {
        background: radial-gradient(ellipse at 10% 0%, #19243a 0%, #0b1020 42%, #080b13 100%);
        color: #f3f5fb;
      }
      [data-testid="stSidebar"] {
        background: rgba(13, 19, 33, 0.96);
        border-right: 1px solid rgba(255,255,255,0.08);
      }
      .block-container { padding-top: 5rem; padding-bottom: 3rem; max-width: 1180px; }
      .eyebrow {
        color: #9daefb; font-size: 0.76rem; font-weight: 750;
        letter-spacing: 0.16em; text-transform: uppercase; margin-bottom: 0.5rem;
      }
      .hero-title { font-size: clamp(2.1rem, 5vw, 3.5rem); line-height: 1.04;
        letter-spacing: -0.045em; font-weight: 800; margin: 0; }
      .hero-subtitle { color: #aab4ca; font-size: 1.02rem; margin-top: 0.85rem; max-width: 720px; }
      .stage-card {
        padding: 1rem 1.1rem; border: 1px solid rgba(255,255,255,0.10);
        background: rgba(255,255,255,0.035); border-radius: 15px; min-height: 112px;
      }
      .stage-number { color: #a6b4ff; font-size: 0.76rem; font-weight: 800; letter-spacing: .09em; }
      .stage-title { color: #f4f6ff; font-weight: 750; font-size: 1.02rem; margin-top: .35rem; }
      .stage-caption { color: #9ea9c0; font-size: .85rem; margin-top: .25rem; }
      .section-title { font-size: 1.18rem; font-weight: 750; margin: .3rem 0 .35rem 0; }
      div[data-testid="stTextArea"] textarea {
        background: #0e1524; color: #f1f4fc; border: 1px solid #29344c; border-radius: 12px;
      }
      div[data-testid="stButton"] > button[kind="primary"] {
        border: 0; color: #0b1020; font-weight: 800; min-height: 3rem;
        background: linear-gradient(100deg, #a6b4ff 0%, #81e6d9 100%);
        border-radius: 11px;
      }
      div[data-testid="stButton"] > button { border-radius: 10px; }
      div[data-testid="stTabs"] button { font-weight: 700; }
      .small-muted { color: #9ea9c0; font-size: .88rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown("### ✦ Script Studio")
    st.caption("AI-powered script transformation")
    st.divider()
    st.markdown("**Your workflow**")
    st.markdown("1. Clean up raw text")
    st.markdown("2. Write an engaging video script")
    st.markdown("3. Localize it into natural Hinglish")
    st.divider()
    st.markdown("**Model**")
    st.code("openai/gpt-oss-20b", language=None)
    st.caption("Powered by LangGraph + Groq")

st.markdown('<div class="eyebrow">Your AI writing workspace</div>', unsafe_allow_html=True)
st.markdown('<h1 class="hero-title">From raw text to<br>ready-to-speak script.</h1>', unsafe_allow_html=True)
st.markdown(
    '<p class="hero-subtitle">A three-stage workflow that polishes your text, gives it a compelling video-script flow, and adapts it into conversational Hinglish.</p>',
    unsafe_allow_html=True,
)
st.write("")

stage_cols = st.columns(3, gap="medium")
stages = [
    ("STAGE 01", "Copyeditor", "Grammar, spelling, and clarity"),
    ("STAGE 02", "Scriptwriter", "Punchy, conversational delivery"),
    ("STAGE 03", "Hinglish translator", "Natural Hindi + English flow"),
]
for col, (number, title, caption) in zip(stage_cols, stages):
    with col:
        st.markdown(
            f'<div class="stage-card"><div class="stage-number">{number}</div>'
            f'<div class="stage-title">{title}</div><div class="stage-caption">{caption}</div></div>',
            unsafe_allow_html=True,
        )

st.write("")
left, right = st.columns([1.12, 0.88], gap="large")
with left:
    st.markdown('<div class="section-title">Start with your raw text</div>', unsafe_allow_html=True)
    st.markdown('<div class="small-muted">Paste narration, notes, or a rough draft. Keep the original meaning; the pipeline will handle the rest.</div>', unsafe_allow_html=True)

    if "raw_input" not in st.session_state:
        st.session_state.raw_input = ""

    def load_example():
        st.session_state.raw_input = EXAMPLE_TEXT

    st.button("Load example", on_click=load_example, use_container_width=False)
    raw_text = st.text_area(
        "Raw text",
        key="raw_input",
        height=255,
        placeholder="Paste your text here...",
        label_visibility="collapsed",
    )
    run_clicked = st.button(
        "Generate my script  →",
        type="primary",
        use_container_width=True,
        disabled=not raw_text.strip(),
    )

with right:
    st.markdown('<div class="section-title">What you’ll get</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="stage-card" style="min-height:255px">
          <div class="stage-title">One input. Three useful outputs.</div>
          <p class="stage-caption" style="line-height:1.8;margin-top:.8rem">
            <b style="color:#e8ebfa">Edited text</b><br>Clean and easy to follow.<br><br>
            <b style="color:#e8ebfa">Video script</b><br>Engaging, spoken-word style.<br><br>
            <b style="color:#e8ebfa">Final Hinglish</b><br>Natural for an Indian audience.
          </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.caption("Each stage runs in sequence using your LangGraph pipeline.")

if run_clicked:
    if not os.getenv("GROQ_API_KEY"):
        st.error("GROQ_API_KEY was not found. Add it to a .env file in the same folder as app.py, then restart Streamlit.")
        st.stop()

    try:
        pipeline = build_pipeline()
        outputs = {
            "edited_text": "",
            "script_text": "",
            "final_output": "",
        }
        progress = st.progress(0, text="Preparing your workflow...")
        status_box = st.status("Generating your script...", expanded=True)
        node_details = {
            "editor": (1, "Copyeditor", "Cleaning up grammar and flow"),
            "scriptwriter": (2, "Scriptwriter", "Making the text engaging and conversational"),
            "translater": (3, "Hinglish translator", "Localizing the script into natural Hinglish"),
        }

        with status_box:
            for update in pipeline.stream({"raw_input": raw_text.strip()}, stream_mode="updates"):
                for node_name, node_result in update.items():
                    if node_name in node_details:
                        stage_num, label, detail = node_details[node_name]
                        outputs.update(node_result or {})
                        progress.progress(stage_num / 3, text=f"Stage {stage_num} of 3 · {label}")
                        st.write(f"**Stage {stage_num}: {label}** — {detail}")

        status_box.update(label="Your script is ready", state="complete", expanded=False)
        progress.progress(1.0, text="All three stages completed")
        st.session_state.pipeline_outputs = outputs
        st.session_state.pipeline_source = raw_text.strip()
        # Refresh the keyed result text areas when a new run completes.
        st.session_state["result_edited"] = outputs.get("edited_text", "")
        st.session_state["result_script"] = outputs.get("script_text", "")
        st.session_state["result_hinglish"] = outputs.get("final_output", "")
        st.success("Script generation completed.")
    except Exception as exc:
        st.error(f"The pipeline failed: {exc}")
        st.caption("Check your API key, installed dependencies, and the terminal for the detailed error.")

# Keep the latest generated result visible on normal Streamlit reruns.
outputs = st.session_state.get("pipeline_outputs")
if outputs:
    st.divider()
    st.markdown('<div class="section-title">Your generated results</div>', unsafe_allow_html=True)
    st.markdown('<div class="small-muted">Review each stage, then download the version you need.</div>', unsafe_allow_html=True)

    tab_edited, tab_script, tab_hinglish = st.tabs(
        ["01 · Edited text", "02 · Video script", "03 · Final Hinglish"]
    )
    with tab_edited:
        st.text_area("Edited text result", value=outputs.get("edited_text", ""), height=260, key="result_edited")
        st.download_button(
            "Download edited text (.txt)",
            data=outputs.get("edited_text", ""),
            file_name="edited_text.txt",
            mime="text/plain",
        )
    with tab_script:
        st.text_area("Video script result", value=outputs.get("script_text", ""), height=260, key="result_script")
        st.download_button(
            "Download video script (.txt)",
            data=outputs.get("script_text", ""),
            file_name="video_script.txt",
            mime="text/plain",
        )
    with tab_hinglish:
        st.text_area("Final Hinglish result", value=outputs.get("final_output", ""), height=260, key="result_hinglish")
        st.download_button(
            "Download Hinglish script (.txt)",
            data=outputs.get("final_output", ""),
            file_name="hinglish_script.txt",
            mime="text/plain",
        )

    all_text = (
        "STAGE 1 — EDITED TEXT\n\n" + outputs.get("edited_text", "")
        + "\n\n\nSTAGE 2 — VIDEO SCRIPT\n\n" + outputs.get("script_text", "")
        + "\n\n\nSTAGE 3 — FINAL HINGLISH\n\n" + outputs.get("final_output", "")
    )
    st.download_button(
        "Download all stages (.txt)",
        data=all_text,
        file_name="script_studio_results.txt",
        mime="text/plain",
        type="primary",
    )
else:
    st.divider()
    st.info("Your generated outputs will appear here after you run the pipeline.")
