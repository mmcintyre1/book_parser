from bs4 import BeautifulSoup
import ebooklib
from ebooklib import epub
import pathlib
from PyPDF2 import PdfFileReader
import sys
import textstat


class BookTypeError(Exception):
    pass


# controls HTML exclusion elements to remove
# from gathering fulltext for a marked up ebook
HTML_BLACKLIST = [
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

# controls the section elements to remove from the fulltext
# output, such as copyright page or acknowledgments
# this needs to stay a tuple to be ingested with startswith()
SECTION_BLACKLIST = (
    'contents',
    'copyright',
    'dedication',
    'acknowledgment',
    'about the author',
    'about the publisher',
    'also by',
    'index'
)


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
        if t.parent.name not in HTML_BLACKLIST and t.strip()
    ])


def parse_epub(book_location):
    book = epub.read_epub(book_location)
    documents = get_documents(book)
    return [get_text_from_document(doc) for doc in documents if doc]


def parse_pdf(book_location):
    pdf = PdfFileReader(str(book_location))
    return [
        page.extractText()
        for page in pdf.pages
    ]


def get_stats(text):
    print(f"Word Count: {textstat.lexicon_count(text, removepunct=True)}")
    print(f"Flesh-Kincaid Score: {textstat.flesch_reading_ease(text)}")
    print(f"Flesh-Kincaid Grade Level: {textstat.flesch_kincaid_grade(text)}")
    print(f"Reading Level Across Multiple Tests: {textstat.text_standard(text, float_output=False)}")


def main():
    book_in = pathlib.Path(sys.argv[1])
    if book_in.suffix == '.epub':
        all_text = parse_epub(book_in)
    elif book_in.suffix == '.pdf':
        all_text = parse_pdf(book_in)
    else:
        raise BookTypeError(f"{book_in.suffix} not a valid file extension.")

    filtered_text = [
        t
        for t in all_text
        if t and not t.lower().startswith(SECTION_BLACKLIST)
    ]

    # helpful to see the 'chapters' that are returned as text so these can hopefully
    # be removed in the future for a more accurate count
    print("\n".join([t[:150] for t in filtered_text]))
    get_stats(" ".join(filtered_text))


if __name__ == '__main__':
    main()
