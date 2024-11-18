from scipy.stats import hypergeom

from utils import *

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 

class Reference():

    def __init__(self,
                 title : str,
                 reference_dict : dict) -> None:
        
        self.title = title
        self.reference_dict = reference_dict
        
        self.N = 2435129274 
        self.sum = sum(reference_dict.values())

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 

    def get_type_freq(self, word : str) -> int:
        return self.reference_dict.get(word, 0)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 


RAW_TEXT_DATA_TYPE = 'raw_text'
CONCORDANCE_DATA_TYPE = 'concordance'

DATA_TYPES = [RAW_TEXT_DATA_TYPE, CONCORDANCE_DATA_TYPE]

ALPHA_DEFAULT_VALUE = 0.95
MINIMAL_RATIO_DEFAULT_VALUE = 1.

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 

class KeywordExtractor():

    def __init__(self):
        
        # dictionary of references where the key is the reference title
        # and the value is a Reference object
        self.references = {}
        
        # the active reference object
        self.active_reference = None
        
        # the confidence level
        self.set_confidence_level(ALPHA_DEFAULT_VALUE)
        
        # the data type either a concordance (2 columns type and frequency) or raw text
        self.set_data_type(RAW_TEXT_DATA_TYPE)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 

    def add_reference(  self, 
                        reference_title : str,
                        file_path : str):
        
        self.references[reference_title] = self._create_ref_from_file(reference_title,
                                                                      file_path)
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    def select_reference(self, reference_title):
        
        if reference_title not in self.references:
            # TODO: replace with raise ValueError
            print(f'Reference title "{reference_title}" not found')
        else:
            self.active_reference = self.references[reference_title]   

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 

    def get_n_types(self):
        
        if self.active_reference is None:       
            print('No reference selected')
            return 0
        else:
            return self.active_reference.N

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 

    def _handle_concordance_query_text(self,
                                       query_text : str):
        
        query_list = []
               
        for line in query_text.split('\n'):
                word_type = line.split()[0]
                type_freq = int(line.split()[1])
                
                query_list.append([word_type, type_freq])
               
        return query_list

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _handle_raw_text_query_text(self,
                                    query_text : str):
        
        query_text = ''.join(filter(lambda x: x.isalpha() or x.isspace(), query_text))
        query_text = query_text.lower() 
        
        word_counts = {}
        for word in query_text.split():
            word_counts[word] = word_counts.get(word, 0) + 1
        
        return [[word, count] for word, count in word_counts.items()]

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _get_query_list(self,
                        query_text : str):        
        
        query_list = []
        
        if self.data_type == CONCORDANCE_DATA_TYPE:
            query_list = self._handle_concordance_query_text(query_text)    
                
        elif self.data_type == RAW_TEXT_DATA_TYPE:
           query_list = self._handle_raw_text_query_text(query_text)
        else:
            #TODO: replace with raise Error
            print(f'Invalid data type: {self.data_type}')
        
        return query_list

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 

    def set_data_type(  self, 
                        data_type : str):

        if data_type in DATA_TYPES:
            self.data_type = data_type
        else:
            # TODO: chanve to raise ValueError
            print(f'Invalid data type: {data_type}')

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    def set_confidence_level(self, 
                             alpha : float):
        self.alpha = alpha
    
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
       
    def _get_cutoff_value(self):
    
        return (1. - self.alpha) / 2.

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 

    def _get_n_sample(self,
                      query_list): 
        
        n_sample = 0
        
        for query in query_list:
            n_sample += query[1]
        
        return n_sample

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
    
    def analyze_text(self,
                     text : str):
        
        query_list = self._get_query_list(text)  
        
        n_sample = self._get_n_sample(query_list)
        
        results = []       
    
        for query in query_list:          
       
            mr, ll, ul = self.calculate_minimal_ratio(  type=query[0],
                                                        type_freq=query[1],
                                                        sample_size=n_sample)
                
            results.append((query[0], mr, query[1], self.get_type_freq(query[0]), ll, ul))
            
        return results

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def extract_keywords(self, 
                         text : str):
    
        results = self.analyze_text(text)
        
        keywords = []
        
        for result in results:
            if result[1] > 1.:
                keywords.append((result[0], result[1]))
        
        return keywords

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def calculate_minimal_ratio(self,
                                type : str,
                                type_freq : int,
                                sample_size : int):
        
        # calculate hypergeometric and search parameters 
        cutoff = self._get_cutoff_value()
        max_i = type_freq + self.active_reference.get_type_freq(type)

        # population size
        M = self.active_reference.N + sample_size
        # number of successes in population
        n = type_freq + self.active_reference.get_type_freq(type)
        # number of samples (# of draws)
        N = sample_size
        
        # calculate lower and upper limits
        ll = self._calculate_lower_limit(M,n,N,max_i)
        ul = self._calculate_upper_limit(M,n,N,max_i)
        
        # test if the type frequency is within the lower and upper limits
        minimal_ratio = MINIMAL_RATIO_DEFAULT_VALUE
        if type_freq < ll:
            minimal_ratio = type_freq / ll
        elif type_freq > ul:
            minimal_ratio = type_freq / (ul+1)

        return minimal_ratio, ll, ul  
      
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
     
    def _calculate_lower_limit( self,
                                M : int, # population size
                                n : int, # number of successes in population
                                N : int, # number of samples (# of draws)
                                max_i : int):
        lower_limit = 0
       
        cumulative_p_value = 0.

        for z_i in range(0,max_i):
                                    
            # cumulative_p_value = hypergeom.cdf(z_i, M, n, N)
            cumulative_p_value = cumulative_p_value + hypergeom.pmf(z_i, M, n, N)
  
            if cumulative_p_value > self._get_cutoff_value():
                break
            else:
                lower_limit = z_i
        
        
        return lower_limit
        
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
        
    def _calculate_upper_limit( self,
                                M : int, # population size
                                n : int, # number of successes in population
                                N : int, # number of samples (# of draws)
                                max_i : int):
        
        upper_limit = 0
            
        for z_i in range(0,max_i):
                                    
            cumulative_p_value = 1. - hypergeom.cdf(z_i, M, n, N)

            if cumulative_p_value < self._get_cutoff_value():
                break
            else:
                upper_limit = z_i
                            
        return upper_limit
    
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
        
    def get_type_freq(  self, 
                        word : str):
        
        if self.active_reference is None:
            # TODO: replace with raise ValueError
            print('No reference selected')
        else:
            return self.active_reference.get_type_freq(word)
   
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
       
    def _create_ref_from_file(self, 
                              reference_title : str, 
                              file_path : str):
        
        reference_dict = {}

        # read reference dictionary from file
        with open(file_path, 'r') as f:
            for line in f:
                line_split = line.split()
                
                if len(line_split) == 2:
                    word, freq = line_split
                    reference_dict[word] = int(freq)
                            
        return Reference(title = reference_title, reference_dict=reference_dict)
    
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
    

  
    