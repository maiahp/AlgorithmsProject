for f in ./datapoints/in*.txt;
do
  python3 basic_3.py $f ./out_basic/out_${f##*/}
  python3 efficient_3.py $f ./out_efficient/out_${f##*/}
done
