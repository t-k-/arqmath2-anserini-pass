anserini="/tuna1/scratch/w32zhong/anserini"
input=$1
output=$2
mkdir -p $output

$anserini/target/appassembler/bin/IndexCollection -collection JsonCollection \
 -input $input \
 -index $output \
 -generator DefaultLuceneDocumentGenerator \
 -threads 16 -storePositions -storeDocvectors -storeRaw -stemmer none -keepStopwords
