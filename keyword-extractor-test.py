from KeywordMinimalRatio.MinimalRatioKeywordExtractor import KeywordExtractor
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download('stopwords')
nltk.download('punkt')

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 

def get_static_query_list():

    return  [   ['debit',303],
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

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 

def get_query_list_from_file(file_path = 'resources/Bus-word-freq-list.txt'):
       
    query_list = []
    
    with open(file_path, 'r') as f:
        
        for line in f:
                
            line_split = line.split()
            
            query_list.append([line_split[0], int(line_split[1])])


    return query_list

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 

def get_sample_size(query_list):
        
    n_sample = 0
    
    for query in query_list:
        n_sample += query[1]
        
    return n_sample

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 

def main():
    
    ke = KeywordExtractor()   
    ke.add_reference('ententen', 'resources/ententen12_lc_freq.txt')
    ke.select_reference('ententen')
    
    print(f'Active reference population size: {ke.active_reference.N}')
   
    query_list = get_static_query_list()
    n_sample = 324035 #get_sample_size(query_list) 
    
    print(f'Query text sample size: {n_sample}')
    
    print(ke.active_reference.sum)

    
    sum_without_stopwords = 0
    stop_words = set(stopwords.words('english'))
    for key in ke.active_reference.reference_dict:
        if key in stop_words:
            continue
        else:
            sum_without_stopwords += ke.active_reference.reference_dict[key]
        
    print(sum_without_stopwords)
    input()
    
    for query in query_list:  
        query_type = query[0]
        query_freq = query[1]
      
        population_freq = ke.get_type_freq(query_type)

        mr, ll, ul = ke.calculate_minimal_ratio(type=query_type, 
                                                type_freq=query_freq,
                                                sample_size=n_sample)
        
        if mr > 1.:
            print(f'{query_type},{mr},{population_freq},{query_freq},{ll},{ul}')
        
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~     

if __name__ == '__main__':
    main()