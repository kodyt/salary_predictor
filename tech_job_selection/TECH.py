import re 
import pandas as pd

file_name = 'salary_state.csv'
column_to_filter = 'job'

def pos_neg_filter():
    data = pd.read_csv(file_name, engine = 'python', error_bad_lines = False)
    
    pos = pd.read_csv('positive.csv').dropna(subset=['Keyword'])
    neg = pd.read_csv('negative.csv').dropna(subset=['Keyword'])

    pos_keys = pos.get('Keyword').tolist()
    pos_keys = [item.lower().strip() for item in pos_keys]


    neg_keys = neg.get('Keyword').tolist()
    neg_keys = [item.lower().strip() for item in neg_keys]


    it_keys = ['it ', ' it', ' it '] #Get IT titles
    
    pos_keys.append('it ')
    pos_keys.append(' it')
    pos_keys.append(' it ')

    pos_keys.append('cto ')
    pos_keys.append(' cto')
    pos_keys.append(' cto ')

    pp = "|".join(pos_keys)
    nn = "|".join(neg_keys)
    
    df = data
    specified_column_1 = column_to_filter #CHANGE SPECIFIED COLUMN HEADER FOR FILTER
    df = df.dropna(subset=[specified_column_1])
    pos_index = []
    neg_index = []

    for col in df[specified_column_1].iteritems():
        pattern = re.compile(pp)
        stri = col[1].lower()
        find_pat = pattern.findall(stri,0,len(stri))
        if len(find_pat) >= 1:
            pos_index.append(col[0])

    df1 = df.loc[pos_index]
    
    for col in df1[specified_column_1].iteritems():
        pattern = re.compile(nn)
        stri = col[1].lower()
        find_pat = pattern.findall(stri,0,len(stri))
        if len(find_pat) >= 1:
            neg_index.append(col[0])
            
    output_1 = df1.drop(index = neg_index)

    unfiltered = df.drop(index = output_1.index)
    
    filtered_name = file_name[:-4] + '_filtered.csv'
    unfiltered_name = file_name[:-4] + '_unfiltered.csv'
	
    output_1.to_csv(filtered_name, index = False)
    unfiltered.to_csv(unfiltered_name,index = False)
    
    
if __name__ == "__main__":
    pos_neg_filter()