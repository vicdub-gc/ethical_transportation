# README for ethical transportation semester project

### Sarah Blanc \& Victor Dubien

The zip contains all the following files :\
-requirements.txt\
-data_final.xlsx\
-PCA_clustering.ipynb\
-most_similar.ipynb\
-most_different.ipynb\
-final.ipynb\
-functions.py\
-trees.pdf\
-report.pdf\
-final_slides.pptx

**requirements.txt** describes the packages you should install in your environment before runnning the code

**data_final.xlsx** contains the raw data collected from the survey

**PCA_clustering.ipynb** contains the code for the correlation, PCA, and clustering methods

**most_similar.ipynb** contains the code for the method removing the outliers by finding the most similar answers among the samples

**most_different.ipynb** contains the code for the method finding the feature that divides best the dataset in two subsets of equal size

**final.ipynb contains** the code combining the two previous notebooks as well as the accuracies (to be read only with the report for full understanding)

**functions.py** contains all functions created and used in the above notebooks. It is important to note the existence of the function called exploreFeature : it allows to visualise and get the majoritarian answer of a subset of samples to any question or scenario. It should be used like this :
exploreFeature(data, subset, 'feature')

**trees.pdf** contains the visualisation of the results, created with *Lucid Charts*

**report.pdf** is simply the report of our semester work.

**final_slides.pptx** contains our presentation for the oral examination.

For further work, if the dataset were to grow for example, the file PCA_clustering.ipynb can be ran fully without any modifications, but the 3 other notebooks would have to be redesigned "by hand" because they are not adaptative. Indeed, because sometimes the branching end and a sample gets isolated, it should not be used fot further calculations because it will not creeat two new subsets. But to continue the branching on the other side, the subset is needed as an input. 
