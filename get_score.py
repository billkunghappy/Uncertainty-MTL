import sys
import json
import matplotlib.pyplot as plt

ALL_SCORE_FILE = "ALL_SCORE.json"
in_file = sys.argv[1]
task = None
only_get_scores = None
FINETUNE=False
if "Finetune" in in_file or "STDNN" in in_file:
    FINETUNE=True
    task = in_file.split("_")[-1].replace(".log","").lower()
    only_get_scores = None
elif len(sys.argv)>2:
    only_get_scores = sys.argv[2]#get epoch
with open(in_file,"r") as F:
	load_data = F.readlines()
# Filter
data = []
for dat in load_data:
	if "Task" in dat and "epoch" in dat and " -- " in dat and "Dev" in dat:
		data.append(dat)


    
all_tasks = [["mnli_matched", "ACC"],
			["mnli_mismatched", "ACC"],
			["rte", "ACC"],
			["qqp", "ACC"],
			["qqp", "F1"],
			["qnli", "ACC"],
			["mrpc", "ACC"],
			["mrpc", "F1"],
			["sst", "ACC"],
			["cola", "ACC"],
			["cola", "MCC"],
			["stsb", "Pearson"],
			["stsb", "Spearman"]]
if task is not None and task != "all":
    use_tasks = []
    for i in all_tasks:
        if task in i[0]:
            use_tasks.append(i)
    all_tasks = use_tasks
epoch = 0
cnt_line = 0
ALL_SCORES = {}
for task in all_tasks:
	ALL_SCORES[task[0]+" "+task[1]]=[]
cnt_task = 0
for line in data:
	task = all_tasks[cnt_task][0]
	metric = all_tasks[cnt_task][1]
	task_str = "Task {} -- epoch {} -- Dev {}: ".format(task, epoch, metric)
	if task_str in line:
		score = float(line.split(task_str)[-1].replace("\n",""))
		ALL_SCORES[task+" "+metric].append(score)
		cnt_task+=1
	if cnt_task == len(all_tasks):
		cnt_task = 0
		epoch += 1

full_epochs = min([len(v) for k,v in ALL_SCORES.items()])

with open(ALL_SCORE_FILE,"r") as F:
    data = json.load(F)
write_key = in_file.split("/")[-1].replace(".log","")
if write_key in data.keys():
    print("ERROR, Alreay have score... \n Write new score...")
data[write_key] = ALL_SCORES
with open(ALL_SCORE_FILE,"w") as F:
    data = json.dump(data, F)



if not FINETUNE:
    if only_get_scores is not None:
        epoch_range = range(only_get_scores, only_get_scores+1)
    else:
        epoch_range = range(full_epochs)

    pairs = [[0,1],[2],[3,4],[5],[6,7],[8],[10],[11,12]]
    key_list = list(ALL_SCORES.keys())
    for get_epoch in epoch_range:
        scores = []
        for p in pairs:
            if len(p)>1:
                scores.append("{} / {}".format(ALL_SCORES[key_list[p[0]]][get_epoch],ALL_SCORES[key_list[p[1]]][get_epoch]))
            else:
                scores.append("{}".format(ALL_SCORES[key_list[p[0]]][get_epoch]))
        print("EPOCH[{}]  ".format(get_epoch) + ",".join(scores))

    if only_get_scores is not None:
        exit(0)
# --------------------------- PLOT ---------------------------------
x = [ i for i in range(full_epochs)]

fig = plt.figure(figsize=(12,8))
if FINETUNE:
    ax = fig.add_subplot(111)
    plt.xticks(range(0,full_epochs,1)) # Redefining x-axis labels

for key, val in ALL_SCORES.items():
    if "rte" in key or "mnli" in key:
        plt.plot(x, val[:full_epochs], label = key, linestyle = "dashed")
    else:
        plt.plot(x, val[:full_epochs], label = key)
    if FINETUNE==True:
        #annotate point y pos
        annot_y = 7
        for i, v in enumerate(val):
            annot_y = -annot_y
            ax.annotate(str("%.2f"%v), xy=(i,v), xytext=(-7,annot_y), textcoords='offset points')
        print("MAX_SCORE[{}] : {}".format(val.index(max(val)),max(val)))
        print(val[:full_epochs])
    
out_name = in_file.split("/")[-1].replace(".log", "")

plt.legend(loc='lower right')
plt.title('[{}] Training Curve'.format(out_name))
plt.xlabel('Epoch')
plt.ylabel('Score')
#plt.savefig("/home/student/06/b06902012/htdocs/imgs/{}.png".format(out_name))
plt.savefig("imgs/{}.png".format(out_name))
