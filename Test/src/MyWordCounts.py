# ADVICE: With PyDev, take care about unused imports (and also unused variables),
# please comment them all, otherwise you will get any errors at the execution.
# Note that even the trick like the directives @PydevCodeAnalysisIgnore and
# @UnusedImport will never solve that issue.
 
# Imports the PySpark libraries
from pyspark import SparkConf, SparkContext
from gc import collect
 
# The 'os' library allows us to read the environment variable SPARK_HOME defined in the IDE environment
import os
import re 

def MapCorrectWords( word ):
        res = (False, 0)
        
        if len(re.findall(".", word, 0)) > 1 :  
            res = (True, word)
              
        return res

# Configure the Spark context to give a name to the application
sparkConf = SparkConf().setAppName("MyWordCounts")
sc = SparkContext(conf = sparkConf)
 
# The text file containing the words to count (this is the Spark README file)
textFile = sc.textFile(os.environ["SPARK_HOME"] + "\README.md")

# The code for counting the words (note that the execution mode is lazy)
# Uses the same paradigm Map and Reduce of Hadoop, but fully in memory
wordCounts = textFile.flatMap(lambda line: line.split(" ")) \
    .map(lambda word: MapCorrectWords(word)) \
    .map(lambda word: (word, 1)) \
    .reduceByKey(lambda a, b: a+b) \
    .map(lambda x : (x[1], x[0])) \
    .sortByKey() \
    .map(lambda x : (x[1], x[0]))
   
# Executes the DAG (Directed Acyclic Graph) for counting and collecting the result
print()
for wc in wordCounts.collect(): print(wc[0][1], " occured", wc[1])
print()