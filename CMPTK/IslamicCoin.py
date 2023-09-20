import re
import unidecode 
import nltk
from nltk import corpus
from nltk import word_tokenize, PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
nltk.download('stopwords')
STOPWORDS = set(stopwords.words('english'))

class IslamicCoinCleaner:
    def __init__(self):
        self.special_tokens = {"coin":" <COIN> ", 
                               "wallet":" <WALLET> ", 
                               "platform":" <PLATFORM> ",
                               "crypto_address":" <ADDRESS> ",
                               "mention":" <MENTION> ",
                               "url": " <URL> ",
                               "hashtag": " <HASHTAG> "}


    def remove_url(self, text, replace_with=None):
        url_pattern = r'https?://\S+|www\.\S+'
        if replace_with is None:
            return re.sub(url_pattern, '', text, flags=re.MULTILINE)
        else:
            return re.sub(url_pattern, replace_with, text, flags=re.MULTILINE)

    def remove_whitespace(self, text):
        """ This function will remove 
            extra whitespaces from the text
        arguments:
            input_text: "text" of type "String". 
                        
        return:
            value: "text" after extra whitespaces removed .
            
        Example:
        Input : How   are   you   doing   ?
        Output : How are you doing ?     
            
        """
        pattern = re.compile(r'\s+') 
        Without_whitespace = re.sub(pattern, ' ', text)
        # There are some instances where there is no space after '?' & ')', 
        # So I am replacing these with one space so that It will not consider two words as one token.
        text = Without_whitespace.replace('?', ' ? ').replace(')', ') ')
        return text

    def remove_links(self, text):
        """
        This function will remove all the occurrences of links.
        
        arguments:
            input_text: "text" of type "String". 
                        
        return:
            value: "text" after removal of all types of links.
            
        Example:
        Input : To know more about this website: kajalyadav.com  visit: https://kajalyadav.com//Blogs
        Output : To know more about this website: visit:     
        
        """
        
        # Removing all the occurrences of links that starts with https
        remove_https = re.sub(r'http\S+', '', text)
        # Remove all the occurrences of text that ends with .com
        remove_com = re.sub(r"\ [A-Za-z]*\.com", " ", remove_https)
        return remove_com

    def remove_newlines_tabs(self, text):
        """
        This function will remove all the occurrences of newlines, tabs, and combinations like: \\n, \\.
        
        arguments:
            input_text: "text" of type "String". 
                        
        return:
            value: "text" after removal of newlines, tabs, \\n, \\ characters.
            
        Example:
        Input : This is her \\ first day at this place.\n Please,\t Be nice to her.\\n
        Output : This is her first day at this place. Please, Be nice to her. 
        
        """
        
        # Replacing all the occurrences of \n,\\n,\t,\\ with a space.
        Formatted_text = text.replace('\\n', ' ').replace('\n', ' ').replace('\t',' ').replace('\\', ' ').replace('. com', '.com').replace('/', '')
        return Formatted_text

    def remove_emoji(self, data):
        emoji_clean= re.compile("["
                    u"\U0001F600-\U0001F64F"  # emoticons
                    u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                    u"\U0001F680-\U0001F6FF"  # transport & map symbols
                    u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                    u"\U00002702-\U000027B0"
                    u"\U000024C2-\U0001F251"
                    u"\U0001f926-\U0001f937"
                    u'\U00010000-\U0010ffff'
                    u"\u200d"
                    u"\u2640-\u2642"
                    u"\u2600-\u2B55"
                    u"\u23cf"
                    u"\u23e9"
                    u"\u231a"
                    u"\u3030"
                    u"\ufe0f"
        "]+", flags=re.UNICODE)

        data=emoji_clean.sub(r'',data)
        url_clean= re.compile(r"https://\S+|www\.\S+")
        data=url_clean.sub(r'',data)
        return data

    def reducing_incorrect_character_repeatation(self, text):
        """
        This Function will reduce repeatition to two characters 
        for alphabets and to one character for punctuations.
        
        arguments:
            input_text: "text" of type "String".
            
        return:
            value: Finally formatted text with alphabets repeating to 
            two characters & punctuations limited to one repeatition 
            
        Example:
        Input : Realllllllllyyyyy,        Greeeeaaaatttt   !!!!?....;;;;:)
        Output : Reallyy, Greeaatt !?.;:)
        
        """
        # Pattern matching for all case alphabets
        Pattern_alpha = re.compile(r"([A-Za-z])\1{1,}", re.DOTALL)
        
        # Limiting all the  repeatation to two characters.
        Formatted_text = Pattern_alpha.sub(r"\1\1", text) 
        
        # Pattern matching for all the punctuations that can occur
        Pattern_Punct = re.compile(r'([.,/#!$%^&*?;:{}=_`~()+-])\1{1,}')
        
        # Limiting punctuations in previously formatted string to only one.
        Combined_Formatted = Pattern_Punct.sub(r'\1', Formatted_text)
        
        # The below statement is replacing repeatation of spaces that occur more than two times with that of one occurrence.
        Final_Formatted = re.sub(' {2,}',' ', Combined_Formatted)
        return Final_Formatted

    def remove_mention(self, text, replace_with=None):
        mention_regex = r'@\w+'
        if replace_with:
            clean_text = re.sub(mention_regex, replace_with, text)
        else:
            clean_text = re.sub(mention_regex, '', text)
        return clean_text

    def clean_hashtags(self, text, replace_with=None):
        # Define a regex pattern to match hashtags
        hashtag_pattern = r'#\w+'

        # Use re.sub to replace all hashtags with an empty string
        if replace_with:
            cleaned_text = re.sub(hashtag_pattern, replace_with, text)
        else:    
            cleaned_text = re.sub(hashtag_pattern, '', text)

        return cleaned_text

    def accented_characters_removal(self, text):
        # this is a docstring
        """
        The function will remove accented characters from the 
        text contained within the Dataset.
        
        arguments:
            input_text: "text" of type "String". 
                        
        return:
            value: "text" with removed accented characters.
            
        Example:
        Input : Málaga, àéêöhello
        Output : Malaga, aeeohello    
            
        """
        # Remove accented characters from text using unidecode.
        # Unidecode() - It takes unicode data & tries to represent it to ASCII characters. 
        text = unidecode.unidecode(text)
        return text

    def to_lower(self, text):
        return text.lower()

    def replace_special_words(self, text):
        text = text.replace('islm coin', ' <COIN> ')
        text = text.replace('islamiccoin', ' <COIN> ')
        text = text.replace('islamic coin', ' <COIN> ')
        text = text.replace('islm', ' <COIN> ')
        text = text.replace('haqq wallet', ' <WALLET> ')
        text = text.replace('haqq network', ' <WALLET> ')
        text = text.replace('haqq', ' <WALLET> ')
        text = text.replace('galxe', ' <PLATFORM> ')
        return text

    def replace_crypto_addresses(self, text, replace_with=None):
        # Define a regex pattern for Ethereum-style addresses
        crypto_address_pattern = r'\b0x[0-9a-fA-F]{40}\b'

        # Use re.sub to replace addresses with "<ADDRESS>"
        if replace_with:
            cleaned_text = re.sub(crypto_address_pattern, replace_with, text)
        else:
            cleaned_text = re.sub(crypto_address_pattern, "", text)

        return cleaned_text
    
    def clean(self, text):
        text = self.to_lower(text)
        text = self.replace_special_words(text)
        text = self.replace_crypto_addresses(text, replace_with=" <ADDRESS> ")    
        text = self.accented_characters_removal(text)
        text = self.remove_url(text, replace_with=" <URL> ")
        text = self.remove_mention(text, replace_with=" <MENTION> ")
        text = self.clean_hashtags(text, replace_with=" <HASHTAG> ")   
        text = self.remove_links(text)
        text = self.remove_newlines_tabs(text)
        text = self.remove_emoji(text)
        text = self.reducing_incorrect_character_repeatation(text)      
        text = self.remove_whitespace(text)
        text = text.strip()
        return text

