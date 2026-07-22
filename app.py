import time

import streamlit as st

from services.rag_service import answer_question


st.set_page_config(
    page_title="Fire Department SOP Assistant",
    page_icon="🚒",
    layout="wide"
)

st.title("🚒 Fire Department SOP Assistant")

st.caption(
    "AI-powered Retrieval-Augmented Generation (RAG) for Fire Department Standard Operating Procedures"
)

question = st.text_area(
    "Ask an operational question",
    placeholder="Example: A worker is trapped inside a manhole. What should firefighters do?",
    height=120
)

if st.button("🔍 Generate Response", use_container_width=True):

    if not question.strip():
        st.warning("Please enter a question.")
        st.stop()

    with st.spinner("Searching SOPs and generating response..."):

        start = time.perf_counter()

        answer, results = answer_question(question)

        elapsed = time.perf_counter() - start

    st.success(f"Response generated in {elapsed:.2f} seconds")

    st.divider()

    st.subheader("🤖 AI Operational Guidance")

    st.write(answer)

    st.divider()

    st.subheader("📚 Retrieved SOPs")

    for result in results:

        with st.expander(
            f"SOG {result['sog_id']} | {result['title']}"
        ):

            st.write(f"**Section:** {result['section']}")

            st.write(
                f"**Similarity Score:** {result['score']:.4f}"
            )

            st.markdown("---")

            st.write(result["text"])