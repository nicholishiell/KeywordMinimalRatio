from scipy.stats import hypergeom

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 

class Reference():

    def __init__(self,
                 title : str,
                 reference_dict : dict) -> None:
        
        self.title = title
        self.reference_dict = reference_dict
        
        self.N = 2435129274 #sum(reference_dict.values())

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 

    def get_type_freq(self, word : str) -> int:
        return self.reference_dict.get(word, 0)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 

class KeywordExtractor():

    def __init__(self):
        self.references = {}
        self.active_reference = None
        self.alpha = 0.95

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

    def calculate_minimal_ratio(self,
                                type : str,
                                type_freq : int,
                                sample_size : int):
        
        ll = self._calculate_lower_limit(type, type_freq, sample_size)
        ul = self._calculate_upper_limit(type, type_freq, sample_size)
        
        minimal_ratio = 1.
        if type_freq < ll:
            minimal_ratio = type_freq / ll
        elif type_freq > ul:
            minimal_ratio = type_freq / (ul+1)

        return minimal_ratio, ll, ul  
      
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
     
    def _calculate_lower_limit( self,
                                type : str,
                                type_freq : int,
                                sample_size : int):
        
        lower_limit = 0
        
        cutoff = (1. - self.alpha) / 2.
        max_i = type_freq + self.active_reference.get_type_freq(type)

        M = self.active_reference.N + sample_size
        N = type_freq + self.active_reference.get_type_freq(type)
        n = sample_size

        for z_i in range(0,max_i):
                                    
            cumulative_p_value = hypergeom.cdf(z_i, M, n, N)
            
            if cumulative_p_value > cutoff:
                break
            else:
                lower_limit = z_i
        
        
        return lower_limit
        
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
        
    def _calculate_upper_limit( self,
                                type : str,
                                type_freq : int,
                                sample_size : int):
        
        upper_limit = 0
        
        cutoff = (1. - self.alpha) / 2.
        max_i = type_freq + self.active_reference.get_type_freq(type)

        M = self.active_reference.N + sample_size
        N = type_freq + self.active_reference.get_type_freq(type)
        n = sample_size
        
        for z_i in range(0,max_i):
                                    
            cumulative_p_value = 1. - hypergeom.cdf(z_i, M, n, N)

            if cumulative_p_value < cutoff:
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
    
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 

def get_guery_list():
    
    query_list = [  ['debit',303],
                    ['column',520],
                    ['merchandise',408],
                    ['accounting',537],
                    ['payable',157],
                    ['salesperson',78],
                    ['accounts',876],
                    ['columns',199],
                    ['totals',78],
                    ['balances',128],
                    ['illustration',156]]
    
    # query_list = []
    
    # with open('resources/windows-exe-output.txt', 'r') as f:
        
    #     for line in f:
                
    #             line_split = line.split()
                
    #             query_list.append([line_split[0], int(line_split[3])])


    return query_list

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 

def main():
    
    query_list = get_guery_list()
    
    ke = KeywordExtractor()   
    ke.add_reference('ententen', 'resources/ententen12_lc_freq.txt')
    ke.select_reference('ententen')
    
    print(f'Active reference population size: {ke.active_reference.N}')
    
    for query in query_list:  
        query_type = query[0]
        query_freq = query[1]
      
        population_freq = ke.get_type_freq(query_type)
        
        mr, ll, ul = ke.calculate_minimal_ratio(type=query_type, 
                                                type_freq=query_freq,
                                                sample_size=324035)
        
        print(f'{query_type},{mr},{population_freq},{query_freq},{ll},{ul}')
        
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~     

if __name__ == '__main__':
    main()
  
    