#!/bin/bash
# Script di avvio dell'applicazione, i parametri
# da specificare sono:
# --graph,-g =  file path
# --heuristic,-h = euristica da utilizzare, possibili valori: [O|E|L|G]
#                  rispettivamente OutDegree,EarlyInfected,LargestInfected,Greedy
#                  default OutDegree
# --delay,-d = int ritardo oltre il quale inizia la campagna buona
# --seed,-s = int numerosita seed di partenza della campagna malevola
# -k = int budget della campagna buona
# --run,-r = int numero di run della simulazione,default 100
# --weighted,-w = [T|F] indica il formato del file
# --randomSeed,-rs = int
function showError {
  echo "Parametro $1 non corretto, deve essere un ";
  exit -1;
}

REGEX_NUMBER='^[0-9]+$'
REGEX_BOOL='[T|F]+$'
REGEX_HEURISTIC='[O|E|L|G]+$'

while [[ $# > 1 ]]
do
key=$1
case $key in
    -g|--graph)
    graph=$2
    shift
    ;;
    -h|--heuristic)
    heuristic=$2
    shift
    ;;
    -d|--delay)
    delay=$2
    shift
    ;;
   -s|--seed)
   seed=$2
   shift
   ;;
   -k)
   k=$2
   shift
   ;;
   --run|-r)
   run=$2
   shift
   ;;
   --weighted|-w)
   w=$2
   shift
   ;;
   --randomSeed|-rs)
   randomSeed=$2
   shift
   ;;
   *)
   echo "Opzione $key sconosciuta"
   exit -1
   ;;
esac
shift
done

#imposto valori di default se necessario e
#verifico la correttezza dei parametri
if [ -z ${graph+x} ]; then echo "Specificare il file contenente il grafo"; exit -1; fi



if [ -z ${w+x} ];
then
  echo "Specificare se il file contiene i pesi sugli archi o meno"
  exit -1;
elif ! [[ $w =~ $REGEX_BOOL ]];then
  showError $weighted "tra T o F"
elif [ "$w" == "T" ];then
  w=1;
else
  w=0;
fi

if [ -z ${run+x} ];
then
  echo "Numero di run non specificato, default 100";
  run=100;
elif ! [[ $run =~ $REGEX_NUMBER ]];then
    showError $run "Numero Intero"
fi


if [ -z ${randomSeed+x} ];then
  randomSeed=-1
fi

for h in $heuristic ; do
  for del in $delay ; do
    for s in $seed ; do
      for budget in $k ; do
        python runner.py $graph $h $del $s $budget $run $randomSeed $w | tail -1 >> results/result.csv
      done
    done
  done
done

echo  "" | mail -a results/result.csv -s "SERVER:Simulazione terminata" calabresematteo@gmail.com,russo.valerio90@gmail.com,antonioc221@gmail.com 
