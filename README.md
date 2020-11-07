# 3D-bin-packing
Refer to the document for problem defination and project description. 

The implementation is partially inspired by (Jiamin Liu, et al., 2011)

Instances ara from : http://people.brunel.ac.uk/~mastjjb/jeb/orlib/conloadinfo.html

# Run the program 
To run the GA, run the "python2 Genetic_AL.py"

In lines 227 - 229 you find these lists:


  * times = [60, 120] : specifies the time limit of the algorithm in seconds (give just one number if you want the algorithm runs once) 

  * filenumbers= [4,5,6,7] : specifies which "Data/wtpack?.txt" files your instace is in. Currently each file has 100 instances 

  * instances=[33,45,52,63,78,84] : specifies which instance inside the file will be solved


# References
1- Liu J., Yue Y., Dong Z., Maple C., Keech M., 2011. "A novel hybrid Tabu Search approach the container loading". Computers & Operations Research 38, 797–807.
