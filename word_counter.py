from bs4 import BeautifulSoup
import ebooklib
from ebooklib import epub
import textstat


BOOK_IN = r"C:\Users\Mike\Desktop\reading_books\2020\A Fans Notes [1968] (Frederick Exley)\A Fans Notes.epub"
PARSING_BLACKLIST = [
    '[document]',
    'noscript',
    'header',
    'html',
    'meta',
    'style',
    'head',
    'input',
    'script',
]


def get_documents(book):
    return [
        doc.get_body_content()
        for doc in book.get_items_of_type(ebooklib.ITEM_DOCUMENT)
    ]


def get_text_from_document(doc):
    soup = BeautifulSoup(doc, 'html.parser')
    text = soup.find_all(text=True)
    return " ".join([
        t.strip()
        for t in text
        if t.parent.name not in PARSING_BLACKLIST and t.strip()
    ])


def get_stats(text):
    print(f"Word Count: {textstat.lexicon_count(text, removepunct=True)}")
    print(f"Flesh-Kincaid Level: {textstat.flesch_kincaid_grade(text)}")
    print(f"Reading Level Across Multiple Tests: {textstat.text_standard(text, float_output=False)}")


def main():
    book = epub.read_epub(BOOK_IN)
    documents = get_documents(book)
    all_text = [get_text_from_document(doc) for doc in documents if doc]

    # helpful to see the 'chapters' that are returned as text so these can hopefully
    # be removed in the future for a more accurate count
    print([t[:50] for t in all_text])

    get_stats(" ".join(all_text))


if __name__ == '__main__':
    main()
