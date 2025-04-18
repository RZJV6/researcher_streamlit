import random
from contextlib import contextmanager, redirect_stdout
from openai import OpenAI
import asyncio
import os
from markdown_pdf import MarkdownPdf, Section
from io import StringIO

from gpt_researcher import GPTResearcher
# from gpt_researcher import DetailedReport
import streamlit as st
from base import *



st.set_page_config(  # https://docs.streamlit.io/develop/api-reference/configuration/st.set_page_config
    page_title="AI GPT Researcher",
    page_icon="assets/gptr-logo.png",
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
                try:
                    if show_logs:
                        st.chat_message("assistant").write(p)
                        st.session_state.messages.append({"role": "assistant", "content": p})
                except:
                    pass
            return ret

        stdout.write = new_write
        yield


output = st.empty()





async def get_report(query: str, report_type: str, tone) -> str:
    if report_type == 'detailed_report':

        # detailed_report = DetailedReport(
        #     query=query,
        #     report_type="research_report",
        #     report_source="web_search",
        # )
        # report = await detailed_report.run()
        pass
    else:
        researcher = GPTResearcher(query, report_type, tone)
        research_result = await researcher.conduct_research()
        report = await researcher.write_report()
    return report


def submit_report(prompt, md_content, msg=None):
    if not msg:
        msg = f"Here is your report base on {os.environ['RETRIEVER']} search"
    st.chat_message("assistant").write(msg)
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("ai").markdown(md_content, unsafe_allow_html=True)
    st.session_state.messages.append({"role": "ai", "content": md_content, "label": "md"})
    make_buttons(prompt, md_content)


def translate_report(prompt, report, lang):
    if lang != "Without translation":
        st.chat_message("assistant").write("Wait 15s for your translated report...")
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system",
                 "content": f'You are professional translator. Translate the user markdown content into language {lang}, while preserving all original markdown syntax. write it without any introductions, just the md content!. If the {lang} language is read from right to left, adjust the markdown formatting accordingly to ensure proper RTL (right-to-left) display.'},
                {"role": "user", "content": f'Here is the markdown content: {report}'}
            ]
        )
        ai_response = response.choices[0].message.content
        ai_response_as_md = ai_response
        if not languages_direction_rtl[lang]:
            prepend_string = '<div style="direction: rtl; text-align: right;">\n\n'
            ai_response_as_md = f"{prepend_string}{ai_response}\n</div>"


        msg = f"Your translated to {lang} report base on {os.environ['RETRIEVER']} search"
        submit_report(prompt, ai_response_as_md, msg)

def translate_question(prompt):
    if translate_question_box:
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system",
                       "content": f'You are professional translator. Translate the user content to English. If the user prompt is already in English, just correct the grammar. Write it without any introductions, just the translated content.'},
                      {"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    return prompt

def chat_ai(prompt, ai_name):
    response = openai_client.chat.completions.create(
        model=ai_name,
        messages=[{"role": "user", "content": prompt}]
    )
    ai_response = response.choices[0].message.content
    st.chat_message("ai").markdown(ai_response)
    st.session_state.messages.append({"role": "ai", "content": ai_response})




def make_buttons(prompt, md_content):
    st.download_button(
        label="Download as Markdown",
        data=md_content,
        file_name=f"{prompt}.md",
        mime="text/markdown",
        key=f'{prompt}-{random.randint(-10 ** 9, 10 ** 9)}'
    )
    st.session_state.messages.append({"role": "ai", "content": md_content,
                                      "label": "Download as Markdown",
                                      "file_name":f"{prompt}.md",
                                      "mime":"text/markdown",
                                      "key" :f'{prompt}-{random.randint(-10 ** 9, 10 ** 9)}'})
    pdf = MarkdownPdf()
    # with open("assets/pdf_styles.css") as css_file:
    #     css = css_file.read()
    pdf.add_section(Section(md_content))
    pdf.writer.close()
    st.download_button(label="Download as PDF",
                       data=pdf.out_file,
                       file_name=f"{prompt}.pdf",
                       mime="application/pdf",
                       key=f'{prompt}-{random.randint(-10 ** 9, 10 ** 9)}')
    st.session_state.messages.append({"role": "ai", "content": pdf.out_file,
                                      "label": "Download as PDF",
                                      "file_name": f"{prompt}.pdf",
                                      "mime": "application/pdf",
                                      "key": f'{prompt}-{random.randint(-10 ** 9, 10 ** 9)}'})






with st.sidebar:
    st.sidebar.html(sidebar_html)
    st.markdown("GPT Researcher is a powerful tool that intelligently searches the web for a research question and summarizes all the sources into a comprehensive academic-style report [(See a demo)](Examples_Page).")

    st.markdown(
        "# How to use\n"
        "1. 🔑 **Enter** your [OpenAI API key](https://platform.openai.com/account/api-keys) below\n"
        "2. ⚙️ **Configure your research:** While you can leave the configuration as default, you can additionally choose the web search engine, report type, and style decide whether to translate the report or view the research process.\n"
        '3. 🔎 **Share your research question:** For example: "Plan a 5 day romantic trip to Paris", "how to optimize my Linkedin profile" or "Nvidia stock analysis"\n'
        "4. 📚 **Get** a comprehensive research report."
    )
    st.markdown("---")
    st.markdown("# Research Setting")

    api_key_input = st.text_input(
        "OpenAI API Key",
        type="password",
        placeholder="Paste your OpenAI API key here (sk-...)",
        help="You can get your API key from https://platform.openai.com/account/api-keys.",  # noqa: E501
        value=st.session_state.get("OPENAI_API_KEY", ""),
    )
    os.environ['OPENAI_API_KEY'] = api_key_input
    st.session_state["OPENAI_API_KEY"] = api_key_input
    openai_client = OpenAI()
    os.environ['RETRIEVER'] = st.selectbox("Choose web search engine", ("duckduckgo", "arxiv",
                                                                           "semantic_scholar"))
    tone = st.selectbox("In which tone would you like the report to be generated?", tone_dict.keys())
    report_type = st.selectbox("What type of report would you like me to generate?", report_type_dict.keys())
    show_logs = st.checkbox("Show the research process (logs)")
    translate_box = st.selectbox("Translate the report to your language", languages_direction_rtl.keys(), help="Select any other language to translate the report into")
    translate_question_box = st.checkbox("Search across the web in English", help= "Use this if your research question is not in English, but you want the research process to involve sources in English")

    st.markdown("---")
    st.markdown("# About")
    st.markdown("""
    - GPT Researcher is an open-source project led by Assaf Elovic and is still in development. This project aims to provide a UI for accessing this amazing tool, and it is based on version 0.9.6.
    - GPT Researcher takes care of everything from accurate source gathering to organization of research results - all in one platform designed to make your research process a breeze.  
    - The average research task takes around 3 minutes to complete, and costs ~$0.005. 
    - [GPT Researcher official page](https://gptr.dev/)
    """)

    st.markdown("---")
    st.markdown("Made with ❤️")
    left, middle, right = st.columns([1,3,1], vertical_alignment="bottom")
    middle.link_button("Invite me for a coffee ☕", "https://ko-fi.com/C0C2125R0E")



st.markdown(header_html_code, unsafe_allow_html=True)


if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hello there"}]
    st.session_state.messages.append({"role": "assistant", "content": "What would you like me to research today?"})

for message in st.session_state.messages:
    if message['role'] == 'ai' and 'label' in message:
        if message['label'] == 'md':
            st.markdown(message['content'], unsafe_allow_html=True)
        else:
            st.download_button(
                label=message['label'],
                data=message['content'],  # The content of the file
                file_name=message['file_name'],  # The name of the file to be downloaded
                mime=message['mime'],  # The MIME type for markdown files
                key=message['key'])
    else:
        st.chat_message(message["role"]).write(message["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    if not api_key_input:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()
    try:
        if report_type_dict[report_type] == "regular AI":
            english_prompt = translate_question(prompt)
            chat_ai(english_prompt,"gpt-4o")
        else:
            english_prompt = translate_question(prompt)
            with stdout_capture(output.code):
                report = asyncio.run(get_report(english_prompt, report_type_dict[report_type], tone))
            try:
                msg = None
                if translate_box != "Without translation":
                    msg = f"your original report base on {os.environ['RETRIEVER']} search"
                submit_report(prompt, report, msg)
                translate_report(prompt, report, translate_box)
            except Exception as exp:
                msg = f"Caught exception submitting the report: {str(exp)}"
                st.error(msg)

    except Exception as e:
        msg = f"Caught exception while searching: {str(e)}"
        st.error(msg)
