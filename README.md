# Uncertainty-MTL
> Contain all results imgs and script
## File structure
### ./imgs
-- 包含所有的圖片，名稱都會是原本 .log 檔變成 .png
### ./*log
-- 所有的log檔，取名規則請執行 get_name.py，照著選，最後用輸出的名稱
### ALL_SCORE.json
-- 存放所有log檔案確切抓出來的成績，是一個 dict，裡面每層的 key 是 log 檔案的名稱去掉 ".log"，每個 item 是那份 log 的成績，也是一個 dict，key 是 TASK+EVAL_METRIC，裡面是存成績的list，依照 epoch 順序
-- 所有的 task 名稱：
* "mnli_mismatched ACC"
* "rte ACC"
* "qqp ACC"
* "qqp F1"
* "qnli ACC"
* "mrpc ACC"
* "mrpc F1"
* "sst ACC"
* "cola ACC"
* "cola MCC"
* "stsb Pearson"
* "stsb Spearman"
## Scripts
### ./get_name.py
-- 用來得到正確名稱的 script
-- 會一步步問你模型的細節，照著選之後會回傳正確檔名，放新的log進來前要改好名稱
-- 裡面比較可能混淆的選項是 Is-Duplicated，這個指的是如果有其他config一模一樣的模型時，會在模型名稱加上"A","B","C" 來區分，目前有的是Random的部分，有重複train
### ./get_score.py
-- 用來畫圖和得到成績的script
-- python3 get_score.py $LOG_FILE
-- 會同步把結果資料加在 ALL_SCORE.json
-- 畫出來的圖會跑到 ./imgs
-- 跑 Finetune 的 log 的時候，最後會輸出最高成績和對應epoch，也會印出每個epoch成績的 list
-- 跑 MTDNN 的 log 的時候，最後會印出每個 epoch 的成績，```可以直接複製貼到excel，選"將文字分隔成不同欄"```
![Image of example](https://github.com/billkunghappy/Uncertainty-MTL/blob/main/%E7%A4%BA%E7%AF%84.png)
-- MTDNN log 可以用 ```python3 get_score.py $LOG_FILE $EPOCH_NUM``` 不畫圖，只取得單個 EPOCH 的成績
### ./draw_all.sh
-- 跑之後會把所有當前資料夾的 log 檔案都跑一次 get_score.py
