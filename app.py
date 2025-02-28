import streamlit as st
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.summarizers.text_rank import TextRankSummarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
import time

st.set_page_config(
    page_title="AI Text Summarizer",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
   .main {
        background-color: #1E1E1E;
        color: #FFFFFF;
    }
    .stTextArea textarea {
        border-radius: 10px;
        border-color: #4A4A4A;
        background-color: #2D2D2D;
        color: #FFFFFF;
        padding: 10px;
    }
    .summary-box {
        background-color: #2D2D2D;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #4A4A4A;
        margin: 10px 0;
        color: #FFFFFF;
    }
    .stButton button {
        border-radius: 20px;
        padding: 10px 25px;
        font-weight: 500;
    }
    .sample-text {
        padding: 10px;
        background-color: #2D2D2D;
        border-radius: 10px;
        margin: 5px 0;
        cursor: pointer;
        color: #FFFFFF;
    }
    .sample-text:hover {
        background-color: #3D3D3D;
    }
    .metrics-box {
        background-color: #2D2D2D;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.3);
        margin: 10px 0;
        color: #FFFFFF;
    }
    /* Make text inputs and text areas more visible */
    textarea, input[type="text"] {
        color: #FFFFFF !important;
        background-color: #2D2D2D !important;
    }
    /* Style for radio buttons text */
    .stRadio label {
        color: #FFFFFF !important;
    }
    /* Style for slider text */
    .stSlider label {
        color: #FFFFFF !important;
    }
    /* Headers and text */
    h1, h2, h3, h4, h5, h6, p {
        color: #FFFFFF !important;
    }
    /* Sidebar text */
    .sidebar .sidebar-content {
        color: #FFFFFF;
    }
    /* Make markdown text visible */
    .stMarkdown {
        color: #FFFFFF;
    }
    @keyframes fadeIn {
        from {opacity: 0;}
        to {opacity: 1;}
    }
    .fade-in {
        animation: fadeIn 1s ease-in;
    }
</style>
""", unsafe_allow_html=True)

def sumy_summarizer(text, summarizer_type="lsa", num_sentences=3):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    
    if summarizer_type == "lsa":
        summarizer = LsaSummarizer(Stemmer("english"))
    elif summarizer_type == "lexrank":
        summarizer = LexRankSummarizer(Stemmer("english"))
    else:
        summarizer = TextRankSummarizer(Stemmer("english"))
    
    summarizer.stop_words = get_stop_words("english")
    
    summary = summarizer(parser.document, num_sentences)
    return " ".join([str(sentence) for sentence in summary])

sample_texts = {
    "Technology": """
    Artificial Intelligence has revolutionized the way we live and work. Machine learning algorithms now power 
    everything from smartphone applications to autonomous vehicles. Deep learning, a subset of AI, has made 
    significant breakthroughs in image recognition, natural language processing, and game playing. As these 
    technologies continue to evolve, they raise important questions about privacy, ethics, and the future of 
    human work. Companies worldwide are investing heavily in AI research and development, leading to rapid 
    advancements in the field. However, concerns about bias in AI systems and their impact on employment 
    remain significant challenges that need to be addressed.
    """,
    
    "Science": """
    Climate change poses one of the greatest challenges to our planet's future. Rising global temperatures 
    have led to melting ice caps, rising sea levels, and more frequent extreme weather events. Scientists 
    have observed significant changes in weather patterns, ecosystem dynamics, and species distribution. 
    The burning of fossil fuels continues to be a major contributor to greenhouse gas emissions, despite 
    growing awareness of its environmental impact. While renewable energy technologies are becoming more 
    efficient and affordable, the transition away from fossil fuels remains a complex global challenge. 
    International cooperation and immediate action are crucial to addressing this pressing environmental issue.
    """,
    
    "Health": """
    The COVID-19 pandemic has transformed global healthcare systems and public health practices. The rapid 
    development of vaccines demonstrated the potential of modern medical research and international 
    collaboration. Healthcare providers have adapted to new challenges through telemedicine and digital 
    health solutions. The pandemic has highlighted existing healthcare disparities and the importance of 
    preparedness for future health crises. Mental health has emerged as a critical concern, with increased 
    recognition of the psychological impact of isolation and uncertainty. These experiences have led to 
    lasting changes in how we approach public health and healthcare delivery.
    """
}

def main():
    st.markdown("<h1 class='fade-in'>📚 AI Text Summarizer</h1>", unsafe_allow_html=True)
    st.markdown("Transform long texts into concise summaries with the power of AI! 🚀")
    
    with st.sidebar:
        st.header("⚙️ Settings")
        
        summarization_type = st.radio(
            "Choose Summarization Method",
            ["LSA (Latent Semantic Analysis)", 
             "LexRank", 
             "TextRank"]
        )
        
        num_sentences = st.slider("Number of Sentences in Summary", 1, 10, 3)
        
        st.markdown("---")
        st.markdown("""
        ### About the Methods
        
        **LSA (Latent Semantic Analysis)**
        - Uses singular value decomposition
        - Good for technical content
        - Captures hidden relationships
        
        **LexRank**
        - Graph-based approach
        - Similar to Google's PageRank
        - Good for news articles
        
        **TextRank**
        - Based on PageRank algorithm
        - Good for natural language
        - Works well with web content
        
        Made with ❤️ by Taha Saif
        """)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Enter Your Text")
        text_input = st.text_area(
            "Paste your text here",
            height=200,
            placeholder="Enter or paste your text here..."
        )
        
        col1_1, col1_2, col1_3 = st.columns(3)
        with col1_1:
            summarize_button = st.button("✨ Summarize", use_container_width=True)
        with col1_2:
            clear_button = st.button("🗑️ Clear", use_container_width=True)
        with col1_3:
            copy_button = st.button("📋 Copy Summary", use_container_width=True)
    
    with col2:
        st.subheader("Sample Texts")
        for title, text in sample_texts.items():
            st.markdown(f"""
            <div class='sample-text' onclick=''>
                <b>{title}</b><br>
                {text[:100]}...
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Use {title} Example", key=title):
                text_input = text
                st.rerun()
    
    if summarize_button and text_input:
        with st.spinner("Generating summary... ⚡"):
            try:
                word_count = len(text_input.split())
                sentence_count = text_input.count('.') + text_input.count('!') + text_input.count('?')
                
                col_m1, col_m2, col_m3 = st.columns(3)
                with col_m1:
                    st.markdown("""
                    <div class='metrics-box'>
                        <h4>Word Count</h4>
                        <p>{}</p>
                    </div>
                    """.format(word_count), unsafe_allow_html=True)
                with col_m2:
                    st.markdown("""
                    <div class='metrics-box'>
                        <h4>Sentence Count</h4>
                        <p>{}</p>
                    </div>
                    """.format(sentence_count), unsafe_allow_html=True)
                with col_m3:
                    st.markdown("""
                    <div class='metrics-box'>
                        <h4>Estimated Read Time</h4>
                        <p>{} min</p>
                    </div>
                    """.format(round(word_count/200, 1)), unsafe_allow_html=True)
                
                summary_type = "lsa" if "LSA" in summarization_type else "lexrank" if "LexRank" in summarization_type else "textrank"
                summary = sumy_summarizer(text_input, summary_type, num_sentences)
                
                st.markdown("### 📝 Summary")
                st.markdown(f"""
                <div class='summary-box fade-in'>
                    {summary}
                </div>
                """, unsafe_allow_html=True)
                
                summary_word_count = len(summary.split())
                reduction = round((1 - summary_word_count/word_count) * 100, 1)
                
                st.markdown(f"""
                <div style='text-align: right; color: #666;'>
                    Summary length: {summary_word_count} words | Reduction: {reduction}%
                </div>
                """, unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    
    if clear_button:
        text_input = ""
        st.experimental_rerun()
    
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        💡 Tip: Try different summarization methods and adjust the number of sentences to find what works best for your text!
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
