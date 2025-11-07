from nltk.tokenize import sent_tokenize

class TextSimplifier:
    """Simplify text for deaf-friendly readability"""
    
    def __init__(self, language='en'):
        self.language = language
    
    def simplify_text(self, text, max_words_per_sentence=15):
        """Break text into short sentences"""
        if not text or len(text.strip()) == 0:
            return ""
        
        try:
            sentences = sent_tokenize(text)
        except:
            sentences = text.split('।')
            if len(sentences) == 1:
                sentences = text.split('.')
        
        if not sentences:
            sentences = [text]
        
        simplified_sentences = []
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
            
            words = sentence.split()
            
            if len(words) > max_words_per_sentence:
                chunks = []
                for i in range(0, len(words), max_words_per_sentence):
                    chunk = ' '.join(words[i:i + max_words_per_sentence])
                    chunks.append(chunk)
                simplified_sentences.extend(chunks)
            else:
                simplified_sentences.append(sentence)
        
        simplified_text = '\n'.join(simplified_sentences)
        return simplified_text