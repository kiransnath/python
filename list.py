#!/usr/bin/python
print "Hello World";
print "\n";
#we can directly assign values. no need to declare the variables in python

inum = 100;
ifloat = 100.0;
istring = "age";

# use format to print the string and numbers 
print "Usage of format to print: Integer is {}, float is {}, String is {}".format(inum,ifloat,istring); 

#Use raw_input to get user input key stroke
raw_input("\n\nThis is using raw_input function for capturing user input. Enter any key to proceed\n\n");

#List can have different data types and we can overwrite the list.
original_list = [0,'test',100.0];
print original_list;
overwritten_list = [1,'test2',200.1];
print overwritten_list;
print "\n";

#We can append to the list using append()
print("Usage of append() function: Appending the word zoo to the above list");
overwritten_list.append('zoo');
print overwritten_list;
print "\n";

#We can pop out the elements using the function pop(). By default the pop function is pointed to -1. ie the last element
poped_element = overwritten_list.pop();
print 'Usage of pop() function: Poped element is {}'.format(poped_element);
print 'Remaining list is {}'.format(overwritten_list);
print "\n";

#Reverse the list use [::-1] function. If you use reverse() function and print it will return None 
new_list = [1,2,3];
print 'Usage of [::-1] to reverse a list: Original list is {}'.format(new_list);
print 'Reversed list is {}'.format(new_list[::-1]);
print 'Printing original list to confirm that its not changed. Original list is {}'.format(new_list);
print "\n";

# Use reversed() function and cast it to list if we want to return the reversed list.
r_list = list(reversed(new_list)); 
print 'Usage of reversed() function: Original list is {}'.format(new_list);
print 'Reversed list is {}'.format(r_list);
print 'Printing original list to confirm that its not changed. Original list is {}'.format(new_list);
print "\n";

# Use reverse() function to reverse but this will not return a list. It overwrites the list.
print 'Usage of reverse() function: Original list is {}'.format(new_list);
new_list.reverse();
print 'Original list is now got overwritten and it is now: {}'.format(new_list);
print '\n';

#Sorting the list use .sort(). Sorts in ascending order
new_list1=[9,8,7];
print 'Usage of sorted() function: Original list is {}'.format(new_list1);
sorted_list = list(sorted(new_list1));
print 'Sorted list is {}'.format(sorted_list);
print 'Printing original list to confirm that its not changed. Original list is {}'.format(new_list1); 
print '\n';

# Use sort() function to sort but this will not return the sorted list back. It overwrites the list.
print 'Usage of sort() function: Original list is {}'.format(new_list1);
new_list1.sort();
print 'Original list is now got overwritten and it is now: {}'.format(new_list1);
print '\n';

#Erasing an element in a list using remove function
new_list = [1,2,3,4,5];
print 'Usage of remove() function: Original list is {}'.format(new_list);
new_list.remove(3);
print 'The list after removing 3 is {}'.format(new_list);
print '\n';

# Nested lists. 
l1 = ['WA','CA','OR'];
l2 = ['Seattle','SFO','Portland'];
l3 = [98007,98008,98009];
matrix = [l1,l2,l3];
print matrix;
print 'Element at first postion of this matrix is [0][0], {}'.format(matrix[0][0]);
print '\n';
print 'To extract the first column of the matrix use row[0] for row in matrix';
first_column = [row[0] for row in matrix];
print first_column;
print '\n';

# Length of the list using ln
print 'Usage of len() function: to find the length of matrix. The lenght is {}'.format(len(matrix));
print '\n';









