for file in ./*.log
do
      python3 get_score.py $file
done
