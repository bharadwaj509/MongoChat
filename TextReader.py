import re
import nltk
from nltk.tokenize import sent_tokenize
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter

class TextProcessor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.sentences = []
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=256,
            chunk_overlap=20,
            separators=[". "]
        )

    def load_and_tokenize(self):
        # Ensure NLTK resources are downloaded
        nltk.download('punkt', quiet=True)

        # Read the text file
        with open(self.file_path, 'r') as file:
            file_content = file.read()


        # Tokenize into sentences
        self.sentences = sent_tokenize(file_content)

    def clean_sentences(self):
        # Define the cleaning function
        def clean_sentence(sentence):
            # Remove numbers in square brackets
            sentence = re.sub(r'\[\d+\]', '', sentence)
            # Trim extra spaces
            sentence = ' '.join(sentence.split())
            return sentence

        # Apply cleaning to each sentence
        self.sentences = [clean_sentence(sentence) for sentence in self.sentences]

    def get_cleaned_sentences(self):
        # Return the cleaned sentences
        return self.sentences

    def get_recursive_splitter(self, sentences):
        text_splitter = CharacterTextSplitter(
            chunk_size=256,
            chunk_overlap=20
        )
        return text_splitter.create_documents([sentences])


# Usage
file_path = 'movies.txt'  # Replace with your file path
processor = TextProcessor(file_path)
processor.load_and_tokenize()

# processor.clean_sentences()
# cleaned_sentences = processor.get_cleaned_sentences()

# # Print cleaned sentences
# for i, sentence in enumerate(cleaned_sentences):
#     print(f"Sentence {i + 1}: {sentence}")
