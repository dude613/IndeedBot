
import spacy

# Load the English language model
nlp = spacy.load("en_core_web_md")

def calculate_sentence_similarity(sentence1, sentence2):
    '''
        A function that uses an ML lib called spacy to 
        get the similarity of words or sentences using their
        meanings
    '''
    # Process the sentences or words with spaCy
    doc1 = nlp(sentence1)
    doc2 = nlp(sentence2)

    # Calculate the similarity between the processed sentences
    similarity_score = doc1.similarity(doc2)

    return similarity_score*100





