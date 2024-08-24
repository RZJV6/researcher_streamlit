import random
from contextlib import contextmanager, redirect_stdout
from openai import OpenAI
import asyncio
import os
from markdown_pdf import MarkdownPdf, Section
from io import StringIO

from gpt_researcher import GPTResearcher
import streamlit as st
from base import *
import pathlib
from bs4 import BeautifulSoup
import shutil
import streamlit.components.v1 as components




st.set_page_config(  # https://docs.streamlit.io/develop/api-reference/configuration/st.set_page_config
    page_title="AI GPT Researcher",
    page_icon="gptr-logo.png",
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



st.markdown("""
<div class="left-ad-div">
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-1699814099300915"
         crossorigin="anonymous"></script>
    <!-- gpt on right -->
    <ins class="adsbygoogle"
         style="display:block"
         data-ad-client="ca-pub-1699814099300915"
         data-ad-slot="7430140409"
         data-ad-format="auto"
         data-full-width-responsive="true"></ins>
    <script>
         (adsbygoogle = window.adsbygoogle || []).push({});
    </script>
</div>
    <style>
        /* CSS for larger screens */
        @media only screen and (min-width: 1100px) {
            .left-ad-div {
                width: 12%;
                height: 100vh; 
                position: fixed; 
                top: 0;
                right: 0;
            }
        }
    </style>
    <script>
            window.onload = function() {
            // Create the meta element
            var meta = document.createElement('meta');
            meta.name = "google-adsense-account";
            meta.content = "ca-pub-1699814099300915";

            // Append the meta element to the head tag
            document.getElementsByTagName('head')[0].appendChild(meta);

            // Create the script element
            var script = document.createElement('script');
            script.async = true;
            script.src = "https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-1699814099300915";
            script.crossOrigin = "anonymous";

            // Append the script element to the head tag
            document.getElementsByTagName('head')[0].appendChild(script);
        }
</script>
""", unsafe_allow_html=True)

async def get_report(query: str, report_type: str, tone) -> str:
    researcher = GPTResearcher(query, report_type, tone, )
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
        st.chat_message("assistant").write("Wait 10s for your translated report...")
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
        if not languages_direction[lang]:
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
    # with open("pdf_styles.css") as css_file:
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

    st.markdown(
        "# How to use\n"
        "1. 🔑 **Enter** your [OpenAI API key](https://platform.openai.com/account/api-keys) below\n"
        '2. 🔎 **Share your research question:** For example: "Plan a 5 day romantic trip to Paris", "how to optimize my Linkedin profile" or "Nvidia stock analysis"\n'
        "3. ⚙️ **Configure your search:** choose your search engine, report type, and style; decide whether to translate the report or view the research process.\n"
        "4. 📚 **Get** a comprehensive research report.\n"

    )
    st.markdown("- [See a demo of the bot's responses](Examples_Page)")
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

    st.markdown("---")
    st.markdown("# Research Setting")
    os.environ['RETRIEVER'] = st.selectbox("Choose your research engine", ("duckduckgo", "arxiv",
                                                                           "semantic_scholar"))
    tone = st.selectbox("In which tone would you like the report to be generated?", tone_dict.keys())
    report_type = st.selectbox("What type of report would you like me to generate?", report_type_dict.keys())
    show_logs = st.checkbox("Show the research process (logs)")
    translate_box = st.selectbox("Translate the report to your language", languages_direction.keys(),help= "Select any other language to translate the report into")
    translate_question_box = st.checkbox("Search across the web in English", help= "Use this if your research question is not in English, but you want the research process to involve sources in English")

    st.markdown("---")
    st.markdown("# About")
    st.markdown("""
    - GPT Researcher takes care of everything from accurate source gathering to organization of research results - all in one platform designed to make your research process a breeze.  
    - GPT Researcher aims to provide you with the most accurate and credible information from multiple online trusted sources, it organize the information and provide you with a comprehensive research report within minutes.  
    - GPT Researcher is still in development and you are welcome to contribute on GitHub. This project aims to provide UI access to this amazing tool.
    - [GPT Researcher official page](https://gptr.dev/)
    """)
    st.markdown("---")

    # st.markdown("Made with ❤️")
    # for Daniela
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
            response = openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )
            ai_response = response.choices[0].message.content
            st.chat_message("ai").markdown(ai_response)
            st.session_state.messages.append({"role": "ai", "content": ai_response})
        else:
            english_prompt = translate_question(prompt)
            # if show_logs:
            with stdout_capture(output.code):
                report = asyncio.run(get_report(english_prompt, report_type_dict[report_type], tone))

            # else:
            #     report = asyncio.run(get_report(english_prompt, report_type_dict[report_type], tone))
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
