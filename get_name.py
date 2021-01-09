Q_flow = {2:["TASK"],
        0:["MTDNN-DESCRIPTION", "Lowest-or-Highest", "Use-Percent-Data","MTDNN-Batch-Size","IF-Duplicated"],
        1:["MTDNN-DESCRIPTION", "Lowest-or-Highest","Use-Percent-Data","MTDNN-Batch-Size","TASK","Finetune-Batch-Size","IF-Duplicated"],
        }
ALL_Q = {"TYPE":[["MTDNN","MTDNN"],["Finetune","Finetune"],["STDNN","STDNN"]],
        "TASK":[["MNLI","MNLI"],["RTE","RTE"],["QQP", "QQP"],["QNLI", "QNLI"],["MRPC", "MRPC"],["SST", "SST"],["COLA", "COLA"],["STSB", "STSB"]],
        "MTDNN-DESCRIPTION":[
            ["Full","FULL"],
            ["Random","R"],
            ["Full-Entropy","[Lowest-or-Highest]E"],
            ["MLM(Bert)-Entropy","MLM[Lowest-or-Highest]E"],
            ["MLM(Bert)-Loss","MLM[Lowest-or-Highest]L"],
            ["LM(GPT)-Entropy","LM[Lowest-or-Highest]E"],
            ["LM(GPT)-Loss","LM[Lowest-or-Highest]L"]
        ],
        "Lowest-or-Highest":[
            ["None", ""],
            ["Lowest", "L"],
            ["Highest", "H"]
        ],
        "Use-Percent-Data":[
            ["100%(Full)",""],
            ["1%", "1"],
            ["5%", "5"],
            ["10%", "10"],
            ["20%", "20"],
            ["50%", "50"]
        ],
        "MTDNN-Batch-Size":[
            ["4", "4"],
            ["8", "8"],
            ["16", "16"],
            ["32", "32"]
        ],
        "Finetune-Batch-Size":[
            ["4", "4"],
            ["8", "8"],
            ["16", "16"],
            ["32", "32"]
        ],
        "IF-Duplicated":[
            ["No Duplicate", ""],
            ["First Duplicate", "A"],
            ["Second Duplicate", "B"],
            ["Third Duplicate", "C"],
        ]



        }
print("Answer the following question, input a number corresponding to the choice idx.")

Answers = []
Q = ["TYPE"]
cnt_Q = 0
while True:
    key = Q[cnt_Q]
    q = "Please select "+key+": \n"
    for i,c in enumerate(ALL_Q[key]):
        q += "({}) {}\n".format(i,c[0])
    if cnt_Q >0:
        q += "(-1) go back to previous question...\n"
    ans = int(input(q))
    #go back
    if ans == -1:
        print("Go back to previous question...")
        if cnt_Q > 0:
            cnt_Q -=1
            del Answers[-1]
            if cnt_Q == 0:#back to select type
                Q = ["TYPE"] #init
        continue

    #invalid input
    elif (ans not in range(len(ALL_Q[key]))):
        print("ERROR, must input right selection, try again...")
        continue
    #valid input
    else:
        if key == "TYPE":
            Q += Q_flow[ans] 
        Answers.append(ans)
        cnt_Q+=1
        print("Select {}: {}".format(key, ALL_Q[key][ans][0]))
        print("-------------------------")
        #Done answer
        if cnt_Q == len(Q):
            break

if Answers[0] == 0:#MTDNN
    FINAL_ANSWER = "MTDNN_[MTDNN-DESCRIPTION][Use-Percent-Data][IF-Duplicated]_[MTDNN-Batch-Size]_ALL.log"
if Answers[0] == 1:#Finetune
    FINAL_ANSWER = "Finetune_[MTDNN-DESCRIPTION][Use-Percent-Data][IF-Duplicated]_[MTDNN-Batch-Size]_[Finetune-Batch-Size]_[TASK].log"
if Answers[0] == 2:#STDNN
    FINAL_ANSWER = "STDNN_[TASK].log"
for a,q in zip(Answers, Q):
    ans_str = ALL_Q[q][a][1]
    FINAL_ANSWER = FINAL_ANSWER.replace("[{}]".format(q),ans_str)
print(FINAL_ANSWER)
