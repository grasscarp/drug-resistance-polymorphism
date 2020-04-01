# drug-resistance-polymorphism
Removing duplications by checking single-resistance polymorphism (SRP).


## step01. choose the sample with least 'U' ('unknown' or 'unclear') as a ref
For example, if one patient has 5 samples that got drug resistance test, we choose the first one:  
ref(1). S S R U S S  
1. S S R U S S  
2. S R R U U S  
3. U S S S U S  
4. S R R U S S  
5. S S R R U U   

## step02. call SRP and count 'U' number
If there is 'U' in ref, we'll keep resistance symbols of all samples at that 'U' position, such as sample 3 and 5.  
ref(1). S S R U S S  
1. - - - - - -  1U  
2. - R - - - -  2U  
3. - - S S - -  2U  
4. - R - - - -  1U  
5. - - - R - -  2U  

## step03. remove the duplications with more 'U'
First, sample 2 will be removed. Secondly, we'll mask the 'U' position and remove once more, so sample 5 will be removed.  
ref(1). S S R U S S  
1. - - - * - -  1U  
3. - - S * - -  2U  
4. - R - * - -  1U  
5. - - - * - -  2U  

The result of removing duplications:  
1. S S R U S S  
3. U S S S U S  
4. S R R U S S  
