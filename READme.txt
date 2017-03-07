Author:
Prateek Singhi
IIIT-H

# Note - The ner-sf-ps folder should be placed in Downloads of the CallHealth Server for running since paths have been set that way.


# RUN
# source startup2.sh 
#// sets the environment variables for Java and also sets the path for classifiers and prop models

# To create the dataset for training run 
#python datacleaning.py > train2.tsv
# To create the dataset for testing at end of file comment the tags and set start and end accordingly
# python datacleaning.py > test2.tsv

# To create your own classifier
# create a prop file similar to those in classifiers folder and write the name of the train file in it (eg. train2.tsv)
# java -cp stanford-ner.jar edu.stanford.nlp.ie.crf.CRFClassifier -prop my1-ner-model.prop
# To test your created classifier 
# java -cp stanford-ner.jar edu.stanford.nlp.ie.crf.CRFClassifier -loadClassifier my1-ner-model.ser.gz -testFile test2.tsv
# copy .ser.gz and .prop to classifiers



# Tokenisers available at
# more modules at http://www.nltk.org/api/nltk.tokenize.html

