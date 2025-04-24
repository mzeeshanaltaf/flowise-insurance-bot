# Import libraries
import streamlit as st

# --- PAGE SETUP ---
main_page = st.Page(
    "main.py",
    title="InsuranceGenie",
    icon=":material/home:", # https://fonts.google.com/icons
    default=True,
)

faq_page = st.Page(
    "faqs.py",
    title="FAQs",
    icon=":material/help:",
)

contact_us = st.Page(
    "contact.py",
    title="Contact Us",
    icon=":material/contact_page:",
)

pg = st.navigation({
    "Home": [main_page],
    "About": [faq_page, contact_us],
                    })

pg.run()