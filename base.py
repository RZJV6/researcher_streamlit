from gpt_researcher.utils.enum import ReportSource, ReportType, Tone

report_type_dict = {"Summary - Short and fast (~2 min)": "research_report",
                    "Resource Report": "resource_report",
                    "Subtopic report":"subtopic_report",
                    "Chat with AI (gpt-4o, without research)": "regular AI"
                    # ,"multi_agents": "multi_agents"
                    # ,"detailed_report":"detailed_report"
                    ,"outline_report":"outline_report"
                    }  # , "multi_agents"


tone_dict = {member.value: member.name for member in Tone}
with open("assets/gptr-logo-base64.txt", "r") as file:
    logo_base64 = file.read()

languages_direction_rtl = {
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

header_html_code = f"""
<div id="responsive-section" align="center">
    <img src="data:image/png;base64,{logo_base64}" width="80"> 
    <h1 style=' text-align: center;'>
        <span style="background-image: linear-gradient(to right, #9867F0, #ED4E50); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">GPT Researcher</span>
    </h1>
    <h2 style="font-weight: 800; text-align: center; line-height: 1.2;">Say Goodbye to Hours of Research</h2>
    <h3 style='text-align: center;'> Say Hello to GPT Researcher, your AI mate for rapid insights and comprehensive research.</h3>
    <p style="text-align: center;  color: gray; margin-top: 0.5em; margin-bottom: 0.5em;">🚀 GPT Researcher unofficial chatbot</p>
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
        div[data-testid="stSidebarNav"]{
            display: none; 
        }
</style>"""

sidebar_html =f"""
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
    </div>"""

# adsence code
# st.markdown("""
# <div class="left-ad-div">
#     <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-1699814099300915"
#          crossorigin="anonymous"></script>
#     <!-- gpt on right -->
#     <ins class="adsbygoogle"
#          style="display:block"
#          data-ad-client="ca-pub-1699814099300915"
#          data-ad-slot="7430140409"
#          data-ad-format="auto"
#          data-full-width-responsive="true"></ins>
#     <script>
#          (adsbygoogle = window.adsbygoogle || []).push({});
#     </script>
# </div>
#     <style>
#         /* CSS for larger screens */
#         @media only screen and (min-width: 1100px) {
#             .left-ad-div {
#                 width: 12%;
#                 height: 100vh;
#                 position: fixed;
#                 top: 0;
#                 right: 0;
#             }
#         }
#     </style>
#     <script>
#             window.onload = function() {
#             // Create the meta element
#             var meta = document.createElement('meta');
#             meta.name = "google-adsense-account";
#             meta.content = "ca-pub-1699814099300915";
#
#             // Append the meta element to the head tag
#             document.getElementsByTagName('head')[0].appendChild(meta);
#
#             // Create the script element
#             var script = document.createElement('script');
#             script.async = true;
#             script.src = "https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-1699814099300915";
#             script.crossOrigin = "anonymous";
#
#             // Append the script element to the head tag
#             document.getElementsByTagName('head')[0].appendChild(script);
#         }
# </script>
# """, unsafe_allow_html=True)