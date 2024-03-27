
# Import the TextProcessor class from the TextReader module
from TextReader import TextProcessor
from TextReaderDic import TextProcessorDic
# Import the TextEmbedder class from the SentenceEmbeddings module
from SentenceEmbeddings import TextEmbedder
import openai
import json


# Specify the path to your text file
file_path = 'movies.txt'  # Update this path as necessary
mongo_url = ""
# mongo url path


# Create an instance of TextProcessor
# processor = TextProcessor(file_path)

# # Load and tokenize the text, then clean the sentences
# processor.load_and_tokenize()
# processor.clean_sentences()

# # Retrieve and print the cleaned sentences
# cleaned_sentences = processor.get_cleaned_sentences()

# merged_sentence = ' '.join(sentence.strip() for sentence in cleaned_sentences)


# split_docs = processor.text_splitter.create_documents([merged_sentence])

# textEmbedder = TextEmbedder(mongo_url)

# embeddings = textEmbedder.generate_embeddings(cleaned_sentences)
# textEmbedder.store_embedding(cleaned_sentences, embeddings)

###########################################################################
###########################################################################
###########################################################################
###########################################################################

file_path = 'movies.txt'  # Replace with your file path
processor = TextProcessorDic(file_path)
sentence_dic = processor.load_and_tokenize()
cleaned_sentences_dic = processor.clean_sentences(sentence_dic)
merged_sentences_dic = processor.merged_sentences(cleaned_sentences_dic)
split_merged_sentences_dic = processor.get_recursive_splitter_dic(merged_sentences_dic)
print("below is the split dic")
print(split_merged_sentences_dic)


textEmbedder = TextEmbedder(mongo_url)
embeddings_dic = {}
# for key, cleaned_sentences in cleaned_sentences_dic.items():
#     embeddings = textEmbedder.generate_embeddings(cleaned_sentences)
#     embeddings_dic[key] = embeddings



# for key, cleaned_sentences in cleaned_sentences_dic.items():
#     textEmbedder.store_embedding_key(key, cleaned_sentences, embeddings_dic[key])


# for key, merged_sentences in merged_sentences_dic.items():
#     embeddings = textEmbedder.generate_embeddings([merged_sentences])
#     embeddings_dic[key] = embeddings



# for key, merged_sentences in merged_sentences_dic.items():
#     textEmbedder.store_embedding_key_fullpage(key, merged_sentences, embeddings_dic[key])


###################################
split_merged_sentences_dic_cleaned = {}
for key, split_sentences in split_merged_sentences_dic.items():
    sentence_list = []
    for sentence in split_sentences:
        sentence_list.append(sentence.page_content)
    split_merged_sentences_dic_cleaned[key] = sentence_list 
    embeddings = textEmbedder.generate_embeddings(sentence_list)
    embeddings_dic[key] = embeddings


for key, sentence_list in split_merged_sentences_dic_cleaned.items():
    textEmbedder.store_embedding_key_fullpage_split(key, sentence_list, embeddings_dic[key])
