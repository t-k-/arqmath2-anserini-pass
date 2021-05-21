set -e
topics="/tuna1/scratch/w32zhong/arqmath/anserini-pass/topics.converted"
indexes="/tuna1/scratch/w32zhong/arqmath/anserini-pass/indexes"
output="/tuna1/scratch/w32zhong/arqmath/anserini-pass/runs"
anserini="/tuna1/scratch/w32zhong/anserini"

n_threads=${1-40}

run() {
	k1=$1
	b=$2
	field=$3
	runfile="$output/arqmath$year/$field.arqmath$year.$task.keepsw.k1=$k1.b=$b.bm25-rm3"
	set -x
	if [[ -e $index_path ]]; then
		sh $anserini/target/appassembler/bin/SearchCollection \
			-index $index_path \
			-topicreader Trec \
			-topics $topic \
			-output $runfile \
			-topicfield $field \
			-inmem -threads $n_threads -keepstopwords -stemmer none \
			-bm25 -bm25.k1 $k1 -bm25.b $b -hits 1000 -rm3
	fi
	set +x
}

for year in 2020 2021; do
	mkdir -p ${output}/arqmath${year}
	for task in task1 task2; do
		index_path="${indexes}/$task"
		refined=""
		if [[ $year == "2020" ]]; then
			topic="${topics}/topics.arqmath-${year}-${task}.txt"
		else
			topic="${topics}/topics.arqmath-${year}-${task}-refined.txt"
		fi
		if [[ $task == "task1" ]]; then
			run 0.9 0.4 title
			run 0.9 0.4 description
			run 0.9 0.4 title+description
			run 1.5 0.75 title
			run 1.5 0.75 description
			run 1.5 0.75 title+description
		else
			run 0.9 0.4 title
			run 1.5 0.75 title
		fi;
	done
done
