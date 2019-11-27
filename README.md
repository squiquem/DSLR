# DSLR

____

How to read a data set, to visualize it in different ways, to select and clean unnecessary information from your data.
How to train a logistic regression that will solve classification problem.

## Run

To describe

	python3 describe.py [-h] file

To visualize

	python3 histogram.py [-h] [-lf] [-o OUTPUT] file
	python3 scatter_plot.py [-h] [-lf] [-o OUTPUT] file
	python3 pair_plot.py [-h] [-o OUTPUT] file
	
To train the model with gradient descent:

	python3 logreg_train.py [-h] [-e EPOCHS] [-lr LEARNINGRATE] [-o OUTPUT] [-st] file

To predict:

	python3 logreg_predict.py [-h] test weights


	positional arguments:
	file                file described
	test        		test file
	weights     		weights file

	optional arguments:
	-h, --help          show this help message and exit
	-lf, --search       plot all 
	-e EPOCHS, --epochs EPOCHS
                        number of iterations
	-lr LEARNINGRATE, --learningrate LEARNINGRATE
                        learning rate
	-o OUTPUT, --output OUTPUT
                        output file
	-st, --stochastic   stochastic gradient descent or not


To eval:

	cd eval
	python3 eval.py dataset_truth.py ../houses.csv

## Screenshots



____

If you have any questions or suggestions, feel free to send me an email at squiquem@student.42.fr
