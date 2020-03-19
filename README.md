# ai-waffle-chef
This friendly AI chef will create brand new waffle recipes based on user input.

## Usage
Clone the package and create a new Python 3.6 environment.
You'll have to use 64-bit Python for Word2Vec to work properly.
Install the required python packages with `pip install -r requirements.txt`.

## Word2Vect Model
We used Google's pretrained Word2Vec model.
It has a vocabulary of 3 million words and was trained on about 100 billion words from a Google News dataset.
Download Google's pretrained model [here](https://drive.google.com/file/d/0B7XkCwpI5KDYNlNUTTlSS21pQmM/) or use your own Word2Vec model.
Put the model in the `data` folder.

Loading Google's pretrained model requires a lot of memory.
If your computer has less memory you can load just part of the model by adding the `limit` argument to the `load_word2vec_format()` function.
The model takes over 7GB of memory to load the full model.
Using `limit=1800000` will cut the memory requirements by about half.

### amount.txt
The file `data/amount.txt` helps the chef determine how much of an ingredient should be added to a recipe.
The number associated with each ingredient is a representation of the ratio of that ingredient with one cup of flour.
1000 represents one cup of the ingredient, so if ingredient X has a score of 500, that means for every cup of flour, there should be about half a cup of ingredient X.
The amounts are a work in progress, so feel free to modify the file according to your needs.

TODO: https://www.tensorflow.org/datasets/catalog/food101