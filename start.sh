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
if [ -z ${delay+x} ];
then
  echo "Specificare il delay della campagna buona"
  exit -1
elif ! [[ $delay =~ $REGEX_NUMBER ]]; then
  showError $delay "Numero intero"
fi

if [ -z ${seed+x} ];
then
  echo "Specificare la numerosita del seed di partenza";
  exit -1;
elif ! [[ $seed =~ $REGEX_NUMBER ]];then
  showError $seed "Numero intero"
fi


if [ -z ${k+x} ];
then
  echo "Specificare il budget";
  exit -1;
elif ! [[ $k =~ $REGEX_NUMBER ]];then
  showError $k "Numero intero"
fi

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

if [ -z ${heuristic+x} ];then
  echo "Euristica non specificata,default out degree";
  heuristic='O'
elif ! [[ $heuristic =~ $REGEX_HEURISTIC ]];then
  showError $heuristic "tra O,E,L,G";
fi

if [ -z ${randomSeed+x} ];then
  randomSeed=-1
fi

arrayArgs=()
arrayArgs+=($graph)
arrayArgs+=($heuristic)
arrayArgs+=($delay)
arrayArgs+=($seed)
arrayArgs+=($k)
arrayArgs+=($run)
arrayArgs+=($randomSeed)
arrayArgs+=($w)

python runner.py ${arrayArgs[@]}  >> log.txt
cat log.txt | tail -1 >> result1.csv
