# Testing

We have included the latest output from the aforementioned pipeline in branch “for testing”, in the directory “testing”. To reproduce our results: 

## generate lemmatizer_test_output_spacy.csv 

* Copy the testing directory from the “for_testing” branch somewhere locally.  

* Checkout to the diverge point
``` 
git checkout 236d32ece893cb2f1d7cd53ac962127c7ba77fb1
``` 

* Add that directory to the new checkout.

* Run
``` 
python spacy_tester.py  
``` 

* Rename the lemmatizer_test_output.csv to lemmatizer_test_output_spacy.csv. Copy that somewhere locally again. 

## generate lemmatizer_test_output.csv 

* Run
``` 
git checkout for_testing 
``` 

* Run
``` 
python spacy_tester.py 
``` 

* Copy to the testing directory the lemmatizer_test_output_spacy.csv 

## compare the results: 

* Now, both the results from the diverged commit and our HEAD are present. 

* Use comparison.py to compare them
``` 
python comparison.py  
``` 

## check the comparison 

* After the comparison, results.txt will have the collective common, spacy and our mistakes.

``` 
cat results.txt 
``` 