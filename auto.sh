_2020_task1_topics=/tuna1/scratch/w32zhong/a0-engine/pya0/topics-and-qrels/topics.arqmath-2020-task1.json
_2020_task2_topics=/tuna1/scratch/w32zhong/a0-engine/pya0/topics-and-qrels/topics.arqmath-2020-task2.txt
_2021_task1_topics=/tuna1/scratch/w32zhong/a0-engine/pya0/topics-and-qrels/topics.arqmath-2021-task1.txt
_2021_task1_topics_refined=/tuna1/scratch/w32zhong/a0-engine/pya0/topics-and-qrels/topics.arqmath-2021-task1-refined.txt
_2021_task2_topics=/tuna1/scratch/w32zhong/a0-engine/pya0/topics-and-qrels/topics.arqmath-2021-task2.txt
_2021_task2_topics_refined=/tuna1/scratch/w32zhong/a0-engine/pya0/topics-and-qrels/topics.arqmath-2021-task2-refined.txt

set -xe
#python prepare_corpus_crys.py --corpus /tuna1/scratch/w32zhong/mnt-corpus-task1.img --output corpus.converted/task1
#python prepare_corpus_crys.py --corpus /tuna1/scratch/w32zhong/mnt-corpus-task2-visual.img --output corpus.converted/task2-visual

python prepare_topic_from_json.py -i $_2020_task1_topics -o topics.converted/$(basename $_2020_task1_topics)
python prepare_topic_from_tsv.py -i $_2020_task2_topics -o topics.converted/$(basename $_2020_task2_topics)
python prepare_topic_from_tsv.py -i $_2021_task1_topics -o topics.converted/$(basename $_2021_task1_topics)
python prepare_topic_from_tsv.py -i $_2021_task1_topics_refined -o topics.converted/$(basename $_2021_task1_topics_refined)
python prepare_topic_from_tsv.py -i $_2021_task2_topics -o topics.converted/$(basename $_2021_task2_topics)
python prepare_topic_from_tsv.py -i $_2021_task2_topics_refined -o topics.converted/$(basename $_2021_task2_topics_refined)
