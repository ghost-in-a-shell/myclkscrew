list1=[1,2,3]
list2=[4,5,6,7,8]
list3=[9]
list4=[10,12]

l1=len(list1)
l2=len(list2)
l3=len(list3)
l4=len(list4)
l=l1*l2*l3*l4
print l

res=[]

for i1 in list1:
	for i2 in list2:
		for i3 in list3:
			for i4 in list4:
				res.append([i1,i2,i3,i4])

print res
with open('paralist','w') as list:
	list.write(str(res))
	
