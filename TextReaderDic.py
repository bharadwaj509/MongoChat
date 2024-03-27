import re
import nltk
from nltk.tokenize import sent_tokenize
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
import json

class TextProcessorDic:
    def __init__(self, file_path):
        self.file_path = file_path
        self.sentences = {}
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=256,
            chunk_overlap=20,
            separators=[". "]
        )

    def load_and_tokenize(self):
        # Ensure NLTK resources are downloaded
        nltk.download('punkt', quiet=True)
        sentences = {}
        # Read the text file
        with open(self.file_path, 'r') as file:
            file_content = file.read()
        # Convert string to JSON
        json_data = json.loads(file_content)
        for key, val in json_data.items():
            # Tokenize into sentences
            sentences[key] = sent_tokenize(val)
        return sentences

    def clean_sentences(self, sentence_dic):
        # Define the cleaning function
        cleaned_sentences_dic = {}
        def clean_sentence(sentence):
            # Remove numbers in square brackets
            sentence = re.sub(r'\[\d+\]', '', sentence)
            # Trim extra spaces
            sentence = ' '.join(sentence.split())
            return sentence

        # Apply cleaning to each sentence
        # self.sentences = [clean_sentence(sentence) for sentence in self.sentences]
        for key, sentences in sentence_dic.items():
            cleaned_sentences = [clean_sentence(sentence) for sentence in sentences]
            cleaned_sentences_dic[key] = cleaned_sentences
        return cleaned_sentences_dic
    
    def merged_sentences(self, cleaned_sentences_dic):
        merged_sentences_dic = {}
        for key, sentences in cleaned_sentences_dic.items():
            merged_sentences = ""
            for sentence in sentences:
                if len(sentence) > 10: 
                    merged_sentences = merged_sentences + " " + sentence.strip()
            merged_sentences_dic[key] = merged_sentences
        return merged_sentences_dic

    def get_recursive_splitter_dic(self, merged_sentences_dic):
        split_merged_sentences_dic = {}
        for key, sentences in merged_sentences_dic.items():
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=256,
                chunk_overlap=20,
                separators=[". "]
            )
            split_merged_sentences_dic[key] = text_splitter.create_documents([sentences])
        return split_merged_sentences_dic


# Usage
file_path = 'movies.txt'  # Replace with your file path
processor = TextProcessorDic(file_path)
sentence_dic = processor.load_and_tokenize()
cleaned_sentences_dic = processor.clean_sentences(sentence_dic)
merged_sentences_dic = processor.merged_sentences(cleaned_sentences_dic)


