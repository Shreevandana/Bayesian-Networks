# Bayesian-Networks

There are three python files inside which do as their namesake:

exact_inference.py
rejection_sampling.py
likelihood_weighting.py
gibbs_sampling.py

Run each file as "python3 file_name.py"

Once executed, the command prompt will ask you for number of evidence variables. 
Enter the number 1,2,3 or 4 depending on the number of evidence variables in the query.

In line 228 of exact inference, tree = ET.parse("aima-alarm.xml”). Change the argument of the parse function to parse whatever file you wish to run. 
In line 208 of rejection sampling and likelihood weighting, tree = ET.parse("aima-alarm.xml”). Change the argument of the parse function to parse whatever file you wish to run. 
In line 258 of gibbs sampling, tree = ET.parse("aima-alarm.xml”). Change the argument of the parse function to parse whatever file you wish to run. 

For example, for the query P(B|J=True,M=True),

For exact inference you will run:
python exact_inference.py aima-alarm.xml B J True M True
and enter “2” when the window prompts you to do so.

For approximate inference you will run:
python likelihood_weighting.py 1000 aima-alarm.xml B J True M True
and enter “2” when the window prompts you to do so.

ADDITIONAL NOTE: Please ensure that the xml files are kept in the same directory as the code.
Please enter the values of evidence variables as only “True” or “False” and NOT “true” and “false”.
