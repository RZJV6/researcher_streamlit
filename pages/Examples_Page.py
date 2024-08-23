import streamlit as st
st.set_page_config(  # https://docs.streamlit.io/develop/api-reference/configuration/st.set_page_config
    page_title="AI GPT Researcher examples",
    page_icon="gptr-logo.png",
    layout="wide",  # optional: you can also use "centered" for a more narrow layout

)
with open("gptr-logo-base64.txt", "r") as file:
    logo_base64 = file.read()

with st.sidebar:
    st.sidebar.html(f"""
    <div id=sidebar align="center">'
        <img src="data:image/png;base64,{logo_base64}" width="80">
        <h1 style='font-size: 2rem;'>
        <span style="background-image: linear-gradient(to right, #9867F0, #ED4E50); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            GPT Researcher
        </span>
        </h1>
        <h2 style="font-size: 1rem; font-weight: 800; text-align: center; line-height: 1.2;">
                The #1 Open Source AI Research Agent
        </h2>
    </div>""")


def show_md(q, md_file_path):
    with open(md_file_path, "r") as file:
        file_content = file.read()
    st.markdown(f"🤔 :orange[{q}]")
    with st.container(height=500):
        st.markdown(file_content)
        st.write("")
        st.write("")


html_code = f"""
<div id="responsive-section" align="center">
    <img src="data:image/png;base64,{logo_base64}" width="80"> 
    <h1 style=' text-align: center;'>
        <span style="background-image: linear-gradient(to right, #9867F0, #ED4E50); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">GPT Researcher</span>
    </h1>
    <h3 style='text-align: center;'>GPT Researcher Usage Examples</h3>
</div>
""" + """
<style>
#responsive-section h1,
#responsive-section h2,
#responsive-section h3,
#responsive-section p { 
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji";
}
#responsive-section h1 {
    font-size: 2.5rem;
}

#responsive-section h2 {
    font-size: 1.5rem;
}

#responsive-section h3 {
    font-size: 1.2rem;
}

#responsive-section p {
    font-size: 0.75em;
}


/* Responsive adjustments */
@media (max-width: 600px) {
    #responsive-section h1 {
        font-size: 2rem; !important;
    }
    #responsive-section h2 {
        font-size: 1.3rem; !important;
    }
    #responsive-section h3 {
        font-size: 1rem; !important;
    }
    #responsive-section p {
        font-size: 0.56em; !important;
    }
    #responsive-section img {
        max-width: 70px; !important;
    }
    #responsive-section {
        padding: 0.5em; !important;
    }
}
</style>"""
st.markdown(html_code, unsafe_allow_html=True)

show_md( "Nvidia stock analysis","assets/Nvidia stock analysis.md")
show_md("how love effect on our health?", "assets/how love effect on our health_.md")
show_md("Berkeley's philosophy towards the discussion of whether morality is objective or relative",
        "assets/Berkeley's philosophy.md")
show_md("What is the security and Weaknesses of the BlockDAG Protocol?", "assets/blockdag sec.md")
show_md("What is the best way to sample in agriculture field?", "assets/sample in agriculture field.md")

# from weasyprint import HTML, CSS
#
# # Specify the HTML file and the CSS file
# html_file = 'html'
# css_file = 'pdf_styles.css'
#
# # Convert HTML to PDF
# HTML(html_file).write_pdf('output.pdf', stylesheets=[CSS(css_file)])
# from xhtml2pdf import pisa
#
# def convert_html_to_pdf(source_html, output_filename):
#     # Open the HTML file and read its content
#     with open(source_html, 'r', encoding='utf-8') as html_file:
#         html_content = html_file.read()
#     with open("pdf_styles.css") as css_file:
#         css = css_file.read()
#     # html_content += "<style> " + css + "</style>"
#
#     # Open the output file in write-binary mode
#     with open(output_filename, 'wb') as pdf_file:
#         # Convert HTML to PDF
#         pisa_status = pisa.CreatePDF(html_content, dest=pdf_file, default_css=css)
#
#     # Check for errors
#     if pisa_status.err:
#         print("Error occurred while converting HTML to PDF")
#     else:
#         print(f"PDF generated successfully: {output_filename}")
#
# # Example usage
# convert_html_to_pdf('html', 'output.pdf')


