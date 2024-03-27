from langchain_community.document_loaders import UnstructuredFileLoader
from unstructured.cleaners.core import clean_extra_whitespace, index_adjustment_after_clean_extra_whitespace, group_broken_paragraphs
import json

pdf_file_path = 'intro.pdf'

loader = UnstructuredFileLoader(pdf_file_path, mode="elements", post_processor=[group_broken_paragraphs])

docs = loader.load()
content = ""


# print(docs)


length = len(docs)
i = 1
dic = {}
while i < length:

    if docs[i].metadata["page_number"] in dic:
        dic[docs[i].metadata["page_number"]] = dic[docs[i].metadata["page_number"]] + " " +docs[i].page_content
    else:
        dic[docs[i].metadata["page_number"]] = docs[i].page_content

    # print(docs[i].metadata["category"], docs[i].metadata["page_number"], docs[i].metadata)
    i = i+1

# Write dic as JSON to movies.txt
with open('movies.txt', 'w') as file:
    json.dump(dic, file, indent=4)
    # json.dump(dic, file)