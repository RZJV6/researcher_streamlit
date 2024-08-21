import random
from contextlib import contextmanager, redirect_stdout

from openai import OpenAI
import asyncio
import os
from markdown_pdf import MarkdownPdf, Section
import base64
from io import StringIO
from gpt_researcher.utils.enum import ReportSource, ReportType, Tone
from gpt_researcher import GPTResearcher
import streamlit as st

report_type_dict = {"Summary - Short and fast (~2 min)": "research_report",
                    "Detailed - In depth and longer (~5 min)": "detailed_report",
                    "Resource Report": "resource_report",
                    "Just chat with AI": "regular AI"
                    }  # , "multi_agents"

tone_dict = {member.value: member.name for member in Tone}

languages_direction = {
    "Without translation": True,
    "English": True,
    "Spanish": True,
    "Russian": True,
    "Arabic": False,
    "Mandarin Chinese": True,
    "Hindi": True,
    "Hebrew": False,
    "Portuguese": True,
    "Afrikaans": True,
    "Akan": True,
    "Albanian": True,
    "Amharic": True,
    "Armenian": True,
    "Azerbaijani": True,
    "Balochi": False,
    "Bengali": True,
    "Bosnian": True,
    "Bulgarian": True,
    "Burmese": True,
    "Catalan": True,
    "Cebuano": True,
    "Chewa": True,
    "Chinese": True,
    "Corsican": True,
    "Croatian": True,
    "Czech": True,
    "Danish": True,
    "Dari": False,
    "Dutch": True,
    "Dzongkha": True,
    "Estonian": True,
    "Faroese": True,
    "Fijian": True,
    "Finnish": True,
    "French": True,
    "Galician": True,
    "Georgian": True,
    "German": True,
    "Greek": True,
    "Gujarati": True,
    "Haitian": True,
    "Hausa": True,
    "Hmong": True,
    "Hungarian": True,
    "Icelandic": True,
    "Igbo": True,
    "Indonesian": True,
    "Irish": True,
    "Italian": True,
    "Japanese": True,
    "Javanese": True,
    "Kannada": True,
    "Kazakh": True,
    "Khmer": True,
    "Kinyarwanda": True,
    "Korean": True,
    "Kurdish": True,
    "Lao": True,
    "Latin": True,
    "Latvian": True,
    "Lithuanian": True,
    "Luxembourgish": True,
    "Macedonian": True,
    "Malagasy": True,
    "Malay": True,
    "Malayalam": True,
    "Maltese": True,
    "Maori": True,
    "Marathi": True,
    "Mongolian": True,
    "Nepali": True,
    "Norwegian": True,
    "Odia": True,
    "Pashto": False,
    "Persian": False,
    "Polish": True,

    "Punjabi": True,
    "Quechua": True,
    "Romanian": True,

    "Samoan": True,
    "Sanskrit": True,
    "Serbian": True,
    "Shona": True,
    "Sindhi": False,
    "Sinhala": True,
    "Slovak": True,
    "Slovene": True,
    "Somali": True,
    "Swahili": True,
    "Swedish": True,
    "Tagalog": True,
    "Tajik": True,
    "Tamil": True,
    "Tatar": True,
    "Telugu": True,
    "Thai": True,
    "Tibetan": True,
    "Tigrinya": True,
    "Tongan": True,
    "Tswana": True,
    "Turkish": True,
    "Turkmen": True,
    "Ukrainian": True,
    "Urdu": False,
    "Uzbek": True,
    "Vietnamese": True,
    "Welsh": True,
    "Wolof": True,
    "Xhosa": True,
    "Yiddish": False,
    "Yoruba": True,
    "Zulu": True
}

st.set_page_config(  # https://docs.streamlit.io/develop/api-reference/configuration/st.set_page_config
    page_title="gpt-researcher",
    page_icon="gptr-logo.png",
    # layout="wide",  # optional: you can also use "centered" for a more narrow layout
    initial_sidebar_state="expanded"
)


@contextmanager
def stdout_capture(output_func):
    with StringIO() as stdout, redirect_stdout(stdout):
        old_write = stdout.write

        def new_write(string):
            ret = old_write(string)
            p = stdout.getvalue()
            if p != "\n" and p:
                stdout.seek(0)
                stdout.truncate(0)
                st.chat_message("assistant").write(p)
                st.session_state.messages.append({"role": "assistant", "content": p})
            return ret

        stdout.write = new_write
        yield


output = st.empty()


async def get_report(query: str, report_type: str, tone) -> str:
    researcher = GPTResearcher(query, report_type, tone, )
    research_result = await researcher.conduct_research()
    report = await researcher.write_report()
    return report


def submit_report(prompt, md_content, msg=None):
    if not msg:
        msg = f"here is your report base on {os.environ['RETRIEVER']} search"
    st.chat_message("assistant").write(msg)
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("ai").markdown(md_content, unsafe_allow_html=True)
    st.session_state.messages.append({"role": "ai", "content": md_content, "label": "md"})
    make_buttons(prompt, md_content)


def translate(prompt, md_content, lang):
    if lang != "Without translation":
        client = OpenAI()
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system",
                 "content": f'You are a translator assistant. Translate the user markdown content into language {lang}, while preserving all original markdown syntax. write it without any introductions, just the md content!. If the {lang} language is read from right to left, adjust the markdown formatting accordingly to ensure proper RTL (right-to-left) display.'},
                {"role": "user", "content": f'Here is the markdown content: {md_content}'}
            ]
        )
        # Extract the response
        ai_response = response.choices[0].message.content
        ai_response_as_md = ai_response
        if not languages_direction[lang]:
            prepend_string = '<div style="direction: rtl; text-align: right;">\n\n'
            ai_response_as_md = f"{prepend_string}{ai_response}\n</div>"

        msg = f"your original report base on {os.environ['RETRIEVER']} search"
        submit_report(prompt, md_content, msg)
        msg = f"your translated to {lang} report base on {os.environ['RETRIEVER']} search"
        submit_report(prompt, ai_response_as_md, msg)
    else:
        submit_report(prompt, md_content)


def make_buttons(prompt, md_content):
    st.download_button(
        label="Download as Markdown",
        data=md_content,  # The content of the file
        file_name=f"{prompt}.md",  # The name of the file to be downloaded
        mime="text/markdown",  # The MIME type for markdown files
        key=f'{prompt}-{random.randint(-10 ** 9, 10 ** 9)}'
    )
    pdf = MarkdownPdf()
    with open("pdf_styles.css") as css:
        text = css.read()
        pdf.add_section(Section(md_content), text)
        pdf.writer.close()
        st.download_button(label="Download PDF",
                           data=pdf.out_file,
                           file_name=f"{prompt}.pdf",
                           mime="application/pdf",
                           key=f'{prompt}-{random.randint(-10 ** 9, 10 ** 9)}')


def get_image_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()


with st.sidebar:
    st.sidebar.header(f'![](gptr-logo.png) GPT Researcher')
    st.sidebar.header("The #1 Open Source AI Research Agent")
    st.markdown(
        "## How to use\n"
        "1. 🔑 **Enter** your [OpenAI API key](https://platform.openai.com/account/api-keys) below\n"
        '2. 🔎 **Share your research question:** For example: "Plan a 5 day romantic trip to Paris", "how to optimize my Linkedin profile" or "Nvidia stock analysis"\n'
        "3. ⚙️ **Configure your search:** determine your engine, report type and style; choose if you want to additionally translate your response and view the research process.\n"
        "4. 📚 **Get** a comprehensive research report\n"
    )
    api_key_input = st.text_input(
        "OpenAI API Key",
        type="password",
        placeholder="Paste your OpenAI API key here (sk-...)",
        help="You can get your API key from https://platform.openai.com/account/api-keys.",  # noqa: E501
        value=st.session_state.get("OPENAI_API_KEY", ""),
    )
    os.environ['OPENAI_API_KEY'] = api_key_input
    st.session_state["OPENAI_API_KEY"] = api_key_input
    st.markdown("---")
    st.markdown("# Research Setting")
    os.environ['RETRIEVER'] = st.selectbox("choose your research engine", ("duckduckgo", "arxiv",
                                                                           "semantic_scholar"))
    tone = st.selectbox("In which tone would you like the report to be generated?", tone_dict.keys())
    report_type = st.selectbox("What type of report would you like me to generate?", report_type_dict.keys())
    show_logs = st.checkbox("show me the research process")
    translate_box = st.selectbox("translate the report to any language", languages_direction.keys())

    st.markdown("---")
    st.markdown("# About")
    st.markdown(
        "GPT Researcher gathering information from multiple online trusted sources. GPT Researcher aims to provide you with the most accurate and credible information, it organize the information and provide you with a comprehensive research report within minutes. "
    )
    st.markdown("[GPT Researcher official page](https://gptr.dev/)")
    st.markdown("---")
    "Made with ❤️ for Daniela"
    st.link_button("Invite me for a coffee ☕", "https://ko-fi.com/C0C2125R0E")

logo_base64 = get_image_base64("gptr-logo.png")
html_code = f"""
<div style='text-align: center; font-size: 3.5rem; font-family: "Libre Baskerville", serif;'>
    <img src="data:image/png;base64,{logo_base64}" alt="" style="vertical-align: middle; ">
    GPT Researcher
</div>
"""
# Display the content using st.markdown
st.markdown(html_code, unsafe_allow_html=True)

st.markdown(
    """
    <h1 style="font-size: 2.5rem; font-weight: 800; text-align: center; line-height: 1.2;">
        <span style="background-image: linear-gradient(to right, #9867F0, #ED4E50); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            Say Goodbye to Hours of Research
        </span>
    </h1>
    """,
    unsafe_allow_html=True
)
st.markdown(
    "<div style='text-align: center;  font-size:  1.5rem;  font-family: 'Libre Baskerville', serif;> Say Hello to GPT Researcher, your AI mate for rapid insights and comprehensive research. GPT Researcher takes care of everything from accurate source gathering to organization of research results - all in one platform designed to make your research process a breeze.</div>",
    unsafe_allow_html=True)
st.caption("🚀 GPT Researcher unofficial chatbot - Powered by Streamlit Cloud")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hello there"}]
    st.session_state.messages.append({"role": "assistant", "content": "What a great day!"})
    st.session_state.messages.append({"role": "assistant", "content": "What would you like me to research today?"})

for message in st.session_state.messages:
    if message['role'] == 'ai' and 'label' in message:
        st.markdown(message['content'], unsafe_allow_html=True)
    else:
        st.chat_message(message["role"]).write(message["content"])

if prompt := st.chat_input():
    if not api_key_input:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    try:
        if report_type_dict[report_type] == "regular AI":
            client = OpenAI()
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )
            ai_response = response.choices[0].message.content
            st.chat_message("ai").markdown(ai_response)
            st.session_state.messages.append({"role": "ai", "content": ai_response})
        else:
            if show_logs:
                with stdout_capture(output.code):
                    msg = asyncio.run(get_report(prompt, report_type_dict[report_type], tone))

            else:
                msg = asyncio.run(get_report(prompt, report_type_dict[report_type], tone))
            translate(prompt, msg, translate_box)
    except Exception as e:
        msg = f"Caught app exception: {str(e)}"
        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.chat_message("assistant").write(msg)

        # with open("noname.md",encoding='utf-8') as f:
        #     msg =f.read()
