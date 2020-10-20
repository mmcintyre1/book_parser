from bs4 import BeautifulSoup
import ebooklib
from ebooklib import epub
import textstat


BOOK_IN = r"C:\Users\Mike\Desktop\reading_books\2020\Brief Answers to the Big Questions [2018]\brief_answers_to_the_big_questions.epub"
PARSING_BLACKLIST = [
    '[document]',
    'noscript',
    'header',
    'html',
    'meta',
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
    print(textstat.lexicon_count(text, removepunct=True))
    print(textstat.text_standard(text, float_output=False))


def main():
    book = epub.read_epub(BOOK_IN)
    documents = get_documents(book)
    all_text = " ".join([get_text_from_document(doc) for doc in documents if doc][1:-1])
    get_stats(all_text)


if __name__ == '__main__':
    main()