# frontend/app.py
import streamlit as st
import requests
import pandas as pd

# Поставување на наслов и иконка на страницата
st.set_page_config(
    page_title="Мојата Библиотека",
    page_icon="📚",
    layout="wide"
)

# API базен URL
API_URL = "http://backend:8000/api"

# CSS стилови
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 2rem;
    }
    .book-card {
        padding: 1.5rem;
        border-radius: 0.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
        background-color: #FFFFFF;
        border-left: 5px solid #1E88E5;
    }
    .sidebar-section {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Функции за API
def get_books():
    try:
        response = requests.get(f"{API_URL}/books/")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Грешка при вчитување на книгите: {e}")
        return []

def get_authors():
    try:
        response = requests.get(f"{API_URL}/authors/")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Грешка при вчитување на авторите: {e}")
        return []

def get_genres():
    try:
        response = requests.get(f"{API_URL}/genres/")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Грешка при вчитување на жанровите: {e}")
        return []

def create_book(book_data):
    try:
        response = requests.post(f"{API_URL}/books/", json=book_data)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ Грешка: {e}")
        st.error(f"Грешка при креирање на книга: {e}")
        return False

def update_book(book_id, book_data):
    try:
        response = requests.put(f"{API_URL}/books/{book_id}/", json=book_data)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        st.error(f"Грешка при ажурирање на книга: {e}")
        return False

def delete_book(book_id):
    try:
        response = requests.delete(f"{API_URL}/books/{book_id}/")
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        st.error(f"Грешка при бришење на книга: {e}")
        return False

def create_author(author_data):
    try:
        response = requests.post(f"{API_URL}/authors/", json=author_data)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        st.error(f"Грешка при креирање на автор: {e}")
        return False

def create_genre(genre_data):
    try:
        response = requests.post(f"{API_URL}/genres/", json=genre_data)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        st.error(f"Грешка при креирање на жанр: {e}")
        return False

# Главен наслов
st.markdown('<h1 class="main-header">📚 Мојата Библиотека</h1>', unsafe_allow_html=True)

# Странична лента
with st.sidebar:
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.header("➕ Додади нов автор")
    
    with st.form("author_form", clear_on_submit=True):
        author_name = st.text_input("Име на автор *")
        author_submitted = st.form_submit_button("Зачувај автор")
        
        if author_submitted:
            if not author_name:
                st.error("Ве молам внесете име на авторот")
            else:
                author_data = {"name": author_name}
                if create_author(author_data):
                    st.success("Авторот е успешно додаден!")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.header("🎭 Додади нов жанр")
    
    with st.form("genre_form", clear_on_submit=True):
        genre_name = st.text_input("Име на жанр *")
        genre_submitted = st.form_submit_button("Зачувај жанр")
        
        if genre_submitted:
            if not genre_name:
                st.error("Ве молам внесете име на жанрот")
            else:
                genre_data = {"name": genre_name}
                if create_genre(genre_data):
                    st.success("Жанрот е успешно додаден!")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.header("📖 Додади нова книга")
    
    with st.form("book_form", clear_on_submit=True):
        title = st.text_input("Наслов *")
        
        authors = get_authors()
        author_options = {author["id"]: author["name"] for author in authors}
        author_id = st.selectbox("Автор *", options=list(author_options.keys()), 
                               format_func=lambda x: author_options[x])
        
        isbn = st.text_input("ISBN *")
        summary = st.text_area("Краток опис")
        rating = st.slider("Оценка", 0.0, 5.0, 3.0, 0.1)
        published_year = st.number_input("Година на издавање", min_value=1000, max_value=2100, value=2023)
        
        book_submitted = st.form_submit_button("Зачувај книга")
        
        if book_submitted:
            if not title or not author_id or not isbn:
                st.error("Ве молам пополнете ги задолжителните полиња (*)")
            else:
                book_data = {
                    "title": title,
                    "author": author_id,
                    "isbn": isbn,
                    "summary": summary,
                    "rating": rating,
                    "published_year": published_year,
                    "genres": []
                }
                if create_book(book_data):
                    st.success("Книгата е успешно додадена!")
    st.markdown('</div>', unsafe_allow_html=True)

# Главен дел - Приказ и менаџирање на книгите
st.header("📖 Сите книги")
books = get_books()

if not books:
    st.info("Сеуште нема книги во библиотеката. Додади прва книга!")
else:
    for i, book in enumerate(books):
        with st.container():
            col1, col2 = st.columns([4, 1])
            
            with col1:
                st.markdown(f"""
                <div class="book-card">
                    <h3>{book['title']}</h3>
                    <p><strong>Автор:</strong> {next((author['name'] for author in get_authors() if author['id'] == book['author']), 'Непознат автор')}</p>
                    <p><strong>ISBN:</strong> {book['isbn']}</p>
                    <p><strong>Оценка:</strong> {'⭐' * round(float(book['rating']))} ({book['rating']}/5.0)</p>
                    <p><strong>Година:</strong> {book['published_year']}</p>
                    <p>{book['summary'] or 'Нема опис'}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                if st.button("🗑️ Избриши", key=f"delete_{book['id']}_{i}"):
                    if delete_book(book['id']):
                        st.success("Книгата е успешно избришана!")
                        st.rerun()
                
                if st.button("✏️ Уреди", key=f"edit_{book['id']}_{i}"):
                    st.session_state.editing_book = book['id']
    
    # Форма за уредување (се појавува кога се клика на Уреди)
    if 'editing_book' in st.session_state:
        editing_book_id = st.session_state.editing_book
        editing_book = next((book for book in books if book['id'] == editing_book_id), None)
        
        if editing_book:
            st.subheader(f"Уреди книга: {editing_book['title']}")
            
            with st.form("edit_book_form"):
                edit_title = st.text_input("Наслов *", value=editing_book['title'])
                
                authors = get_authors()
                author_options = {author["id"]: author["name"] for author in authors}
                edit_author_id = st.selectbox("Автор *", 
                                            options=list(author_options.keys()),
                                            index=list(author_options.keys()).index(editing_book['author']),
                                            format_func=lambda x: author_options[x])
                
                edit_isbn = st.text_input("ISBN *", value=editing_book['isbn'])
                edit_summary = st.text_area("Краток опис", value=editing_book['summary'] or "")
                edit_rating = st.slider("Оценка", 0.0, 5.0, float(editing_book['rating']), 0.1)
                edit_published_year = st.number_input("Година на издавање", 
                                                    min_value=1000, max_value=2100, 
                                                    value=int(editing_book['published_year']))
                
                edit_submitted = st.form_submit_button("Зачувај промени")
                cancel_edit = st.form_submit_button("Откажи")
                
                if cancel_edit:
                    del st.session_state.editing_book
                    st.rerun()
                
                if edit_submitted:
                    if not edit_title or not edit_author_id or not edit_isbn:
                        st.error("Ве молам пополнете ги задолжителните полиња (*)")
                    else:
                        updated_data = {
                            "title": edit_title,
                            "author": edit_author_id,
                            "isbn": edit_isbn,
                            "summary": edit_summary,
                            "rating": edit_rating,
                            "published_year": edit_published_year,
                            "genres": editing_book.get('genres', [])
                        }
                        if update_book(editing_book_id, updated_data):
                            st.success("Книгата е успешно ажурирана!")
                            del st.session_state.editing_book
                            st.rerun()

    # Статистика
    st.subheader("📊 Статистика")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Вкупно книги", len(books))
    
    with col2:
        avg_rating = sum(float(book['rating']) for book in books) / len(books) if books else 0
        st.metric("Просечна оценка", f"{avg_rating:.1f} ⭐")
    
    with col3:
        latest_year = max(int(book['published_year']) for book in books) if books else "Нема"
        st.metric("Најнова книга", latest_year)