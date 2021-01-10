import sys
import json

# usage: python test_file_gen.py [test_file] [output_path] 

LABEL_MAP = {
        'mnli': {'0': 'contradiction', '1': 'neutral', '2': 'entailment'},
        'rte': {'0': 'not_entailment', '1': 'entailment'},
        'qnli': {'0': 'not_entailment', '1': 'entailment'},
        }

with open(sys.argv[1], 'r') as F:
    score = json.loads(F.read())

uids = score['uids']
preds = score['predictions']

with open(sys.argv[2], 'w') as F:
    F.write("index\tprediction\n")
    for i in range(len(uids)):
        task = sys.argv[1].split('_')[0]
        if task in LABEL_MAP.keys():
            pred = LABEL_MAP[task][str(preds[i])]
        else:
            pred = str(preds[i])
        F.write(f"{uids[i]}\t{pred}\n")

