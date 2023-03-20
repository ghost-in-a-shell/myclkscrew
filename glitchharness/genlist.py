list1=['0xd0','0xd8','0xe0']
list2=['5']
list3=['7600','7800','8000','8200','8400','8600','8800']
list4=[40000]

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
with open('paralist2','w+') as list:
	list.write(str(res))
	
