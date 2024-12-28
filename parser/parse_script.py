from bs4 import BeautifulSoup, Comment
from lxml import etree
from PyPDF2 import PdfReader, PdfWriter
import requests
import py7zr
from fpdf import FPDF

namespaces = {
        'mw': 'http://www.mediawiki.org/xml/export-0.11/',
        'xsi': 'http://www.w3.org/2001/XMLSchema-instance'
    }

def download_wiki_xml():
    url = "https://s3.amazonaws.com/wikia_xml_dumps/p/pr/projectdeepwoken_pages_current.xml.7z"
    output = "deepwoken_wiki.7z"

    response = requests.get(url)
    if response.status_code == 200:
        with open(output, "wb") as file:
            file.write(response.content)
    else:
        print("Failed to download file.")
        return

    with py7zr.SevenZipFile(output, "r") as zip:
        zip.extractall()


def remove_namespaces(root, key):
    for page in root.xpath(f"//mw:page[mw:ns='{key}']", namespaces=namespaces):
        parent = page.getparent()
        if parent is not None:
            parent.remove(page)


def parse_xml(file):
    root = etree.parse(file).getroot()

    # Removes useless info in wiki
    for key in [-1, 1, -2, 420, 421, 500, 501, 502, 503, 829, 1200, 1201, 2000, 2001, 2901, 110, 111, 6, 7, 12, 13, 2, 3, 15, 11]:
        remove_namespaces(root, key)

    # Removes most tags
    for tag_name in ['id', 'timestamp', 'comment', 'model', 'origin', 'ns', 'format', 'contributor', 'sha1']:
        for element in root.xpath(f"//mw:page//mw:{tag_name}", namespaces=namespaces):
            parent = element.getparent()
            parent.remove(element)

    full_text = "".join(root.xpath('//text()')).strip()
    full_text = BeautifulSoup(full_text, "html.parser")

    for comment in full_text.find_all(string=lambda text: isinstance(text, Comment)):
        comment.extract()

    # Removes more CSS and HTML tags
    tags = ["style", "script", "meta", "link", "iframe", "embed",
            "header", "footer", "nav", "noscript", "input", "button",
            "div", "center", "font", "gallery", "br", "u", "colspan", "Category", "class", "span",
            "image", "File", "sub", "b", "attribute", "trait", "soundcloud", "name"]
    for tag in tags:
        for element in full_text.find_all(tag):
            element.unwrap()

    for element in full_text.find_all():
        if element.string:
            element.string = element.text.strip()

    cleaned_text = full_text.get_text
    cleaned_text = str(cleaned_text).replace("◯", "").replace("|", "").replace("✗", "").replace("}", "").strip()

    return cleaned_text


def write_onto_pdf(text):
    pdf = FPDF()

    pdf.add_page()
    pdf.add_font("NotoSans", "", "NotoSansAdlam-Regular.ttf", uni=True)
    pdf.set_font("NotoSans", size=12)
    pdf.multi_cell(0, 10, text)

    pdf.output("output.pdf")

    input = "output.pdf"
    output = "output2.pdf"

    reader = PdfReader(input)
    writer = PdfWriter()

    # Remove first 102 pages of useless content
    for page_num in range(102, len(reader.pages)):
        writer.add_page(reader.pages[page_num])

    with open(output, "wb") as output_file:
        writer.write(output_file)

download_wiki_xml()
text = parse_xml("deepwoken_wiki")
write_onto_pdf(text)