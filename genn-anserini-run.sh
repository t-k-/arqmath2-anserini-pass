set -e
topics="/home/x978zhan/task-ict/src/arqmath2021/data/topics-and-qrels"
indexes="/tuna1/scratch/x978zhan/arqmath2021/indexes"
output="/tuna1/scratch/w32zhong/arqmath"
anserini="/tuna1/scratch/w32zhong/anserini"

run() {
	k1=$1
	b=$2
	field=$3
	runfile="$output/runs/arqmath$year/$field.arqmath$year.$task.keepsw.k1=$k1.b=$b.bm25-rm3$refined"
	echo "year=$year, task=$task, field=$3, k1=$k1, b=$b"
	set -x
	sh $anserini/target/appassembler/bin/SearchCollection \
		-index $index_path \
		-topicreader Trec \
		-topics $topic \
		-output $runfile \
		-topicfield $field \
		-inmem -threads 40 -keepstopwords -stemmer none \
		-bm25 -bm25.k1 $k1 -bm25.b $b -hits 1000 -rm3
	set +x
}

for year in 2020 2021; do
	mkdir -p ${output}/runs/arqmath${year}
	for task in task1 task2; do
		index_path="${indexes}/lucene-index.arqmath2021.${task}.pos+docvectors+raw+keepstopwords+nostemmer"
		refined=""
		if [[ $year == "2020" ]]; then
			topic="${topics}/topic.${task}.txt"
		else
			if [[ $task == "task2" ]]; then
				refined=".refined"
			else
				#refined=".refined"
			fi
			topic="${topics}/topics.arqmath-2021-${task}${refined}.converted.txt"
		fi;

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
