import os
import sys
import json
from transformers import BertTokenizer
#Usage: python ./gen_plain.py <dataset> <nbest> <delimeter>

setting = ['withLM', 'noLM']
task = ['train', 'dev', 'test']

assert len(sys.argv == 3), "Usage: python ./gen_plain.py <dataset> <nbest> <delimeter>"

tokenizer = BertTokenizer.from_pretrained('fnlp/bart-base-chinese')

dataset = sys.argv[1]
nbest = sys.argv[2]
delimeter = sys.argv[3]  # delimeter : '#'

delimeter_token = tokenizer.convert_tokens_to_ids(delimeter)

for s in setting:
    for t in task:
        print(f'{s}:{t}')
        with open(f'../data/{dataset}/{s}/{t}/token.json') as f:
            data = json.load(f)

            gen_data = list()

            for d in data:
                tokens = data['token']
                ref_token = data['ref_token']
                ref_text = data['ref']
                ref_token = data['ref_token']

                concat_token = list()

                for i, t in enumerate(tokens):
                    
                    if (i == 0):
                        t[-1] = delimeter_token # [CLS] A B C [SEP] -> [CLS] A B C #
                        concat_token += t # first adding
                    elif i == len(tokens) - 1:
                        concat_token += t[1:] 
                    else:
                        t[-1] = delimeter_token # [CLS] A B C [SEP] -> [CLS] A B C #
                        concat_token += t[1:] # remove [CLS] and concat
                
                gen_data.append(
                    {
                        'token':concat_token,
                        'ref': ref_text,
                        'ref_token': ref_token
                    }
                )
        with open(f'../data/{dataset}/{s}/{t}/{nbest}_plain.json', 'w') as fw:
            json.dump(gen_data, fw, ensure_ascii=False, indent = 4)
