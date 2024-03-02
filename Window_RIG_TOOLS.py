from maya import cmds
from functools import partial

WINDOW_NAME = 'SDrigTools'

def openUi(): 

	if cmds.window(WINDOW_NAME, exists=True) :
		cmds.deleteUI(WINDOW_NAME)

	# curentSel = cmds.ls(sl=True)

	def btnPressed(*arg):


		inputName = cmds.textFieldGrp(locNameInput, query = True, text = True)

		print(inputName)

		print(btnAction)





	def selectPrefixs (*arg): 

		## This is what I made befor the prefixSufix def, it is less complete.

		sel = cmds.ls(sl=True)

		for each_loc in sel:

			## Add the delimiter after each elements:
			# prefix =[x+'_' for x in each_loc.split('_') if x]

			prefix =each_loc.split('_')

			locName = prefix[:-2]

			## Remove the delimiter after the end of the list :
			# locName[-1] = locName[-1].rstrip('_')	

			name = ['_'.join(locName[0:len(locName)])]
			
			return name



	def prefixSufix (element,splitPlace,*arg): 

		### Take an element and split it in a tuple (prefix, sufix):
		## element = input that should be the selected object.
		## splitPos = the place in the list where you whant to separate the prefix and sufix, it uses '_' to do the separations.
		## example of input that take a selected obj and split the start and the 2 last elements (not counting the '_'): 
		## =>     prefixSufix(sel,-2)


		slices = element.split('_')
		objStart = slices[:splitPlace]
		objEnd = slices[splitPlace:]

		prefix = '_'.join(objStart[0:len(objStart)])
		sufix = '_'.join(objEnd[0:len(objEnd)])
			
		return prefix,sufix

		## This can be used to sort element of a list by converting the element befor last to an int, 
		## then sort it out ( ex in : pCube1_009_locPosition it would be '009')

		# sel.sort(key = lambda num:int(num.split('_')[-2]))



	def selectSamePrefix(elements,*arg):


		prefix,sufix = prefixSufix(elements,-2)
		# jName = ''.join(name[0])

		similar = cmds.select (prefix+'_*', r=True)

		return similar
	
		# for e in elements:
		# 	# print(i)
		# 	prefix,sufix = prefixSufix(e,-2)
		# 	# jName = ''.join(name[0])

		# 	cmds.select (prefix+'*', r=True)


	def sortList(elist,place,*arg):

		## This can be used to sort element of a list by converting the element befor last to an int, 
		## then sort it out ( ex in : pCube1_009_locPosition it would be '009')

		# elist.sort(key = lambda num:int(num.split('_')[-2]))

		elist.sort(key = lambda num:int(num.split('_')[place]))
		

		return elist



	def findMidle (element,*args):

		# sel = cmds.ls(sl=True)

		bbox = cmds.exactWorldBoundingBox(element)

		midl = (bbox[3] - bbox[0]) / 2 + bbox[0], (bbox[4] - bbox[1] ) / 2 + bbox[1], (bbox[5] - bbox[2] ) / 2 + bbox[2]

		## Midle Parameters :
		#(midl[0],midl[1], midl[2])
		
		return midl


	def midleLoc(btnAction:str,*arg):

		### Create a locator in the midle with obj name or input name :

		## Button user input base:

		# btnAction text is 'Loc Created'

		inputName = cmds.textFieldGrp(locNameInput, query = True, text = True)
		objName = inputName

		## Button action:

		sel = cmds.ls(sl=True)

		if inputName == "":
				objName = sel[0]

		midl = findMidle(sel)

		## Midle Parameters :
		## (midl[0],midl[1], midl[2])


		if cmds.objExists(objName + '*_locPosition' ):

			cmds.select(objName + '*_locPosition')

			existing = cmds.ls(sl=True)
			exSize = len(existing)

			cmds.spaceLocator(name=objName +'_{0:03d}'.format(exSize + 1)+ '_locPosition'),
			cmds.move(midl[0],midl[1], midl[2], absolute = True)

			sel = cmds.ls(sl=True)

		else:

			loc = cmds.spaceLocator(name=objName+'_001'+ '_locPosition'),
			cmds.move(midl[0],midl[1], midl[2], absolute = True)


		##Button action print (for validation):

		print(btnAction)



	def multiLocs(btnAction:str,*arg):

		# btnAction text is 'Multiples Locs Created'

		sel = cmds.ls(sl=True)

		inputName = cmds.textFieldGrp(locNameInput, query = True, text = True)

		objName = inputName

		for i,each_element in enumerate(sel):

			if inputName == "":
				objName = sel[i]

			midl = findMidle(each_element)

			## Midle Parameters :
			## (midl[0],midl[1], midl[2])

			# inputName = sel[i]
			# if  inputName=="":

			# 	inputName = sel[i]

			

			if cmds.objExists(objName + '*_locPosition' ):

				cmds.select(objName + '*_locPosition')

				existing = cmds.ls(sl=True)
				exSize = len(existing)

				cmds.spaceLocator(name=objName +'_{0:03d}'.format(exSize + 1)+ '_locPosition'),
				cmds.move(midl[0],midl[1], midl[2], absolute = True)

				sel = cmds.ls(sl=True)

			else:

				loc = cmds.spaceLocator(name=objName+'_001'+ '_locPosition'),
				cmds.move(midl[0],midl[1], midl[2], absolute = True)

			print(objName)

		##Button action print (for validation):

		print(btnAction)




	def jntChain(*arg):

	### Create a joint chain from the selected locators parented in order:

		sel = cmds.ls(sl=True)


		for i in sel:

			## Each time makes a sorted list of same prefix objects:

			prefix,sufix = prefixSufix(i,-1)

			selectSamePrefix(i)		
			simili = cmds.ls(sl=True, type='transform')
			sortList(simili,-2)

			## Check if their is a jnt with the same name (go to the next it exist):

			if cmds.objExists(prefix + '_jnt'+'*'):
				continue

			else:

				### Create a joint for each lo then parent them in order:

				for each_loc in simili:
					
					locPrefix= each_loc.split('locPosition')

					cmds.select(each_loc)
					jnt= cmds.joint(n=locPrefix[0] + 'jnt')
					cmds.parent(w=True)
					
				prefix,sufix = prefixSufix(each_loc,-2)
				jnts02 = cmds.ls(prefix +'_'+'*',r=True, type='joint')
				size = len(jnts02)

				for i in range(1, size):
					cmds.parent (jnts02[i], jnts02[i-1])

		cmds.select(sel,r=True)	



	#### Construc the UI:

	win = cmds.window(WINDOW_NAME , title="Rig Tools",wh=(200,200))
	cmds.showWindow(win)

	# grid = cmds.gridLayout(parent=win,numberOfColumns=5)

	column = cmds.columnLayout(adjustableColumn = True)


	## Button to create a loc with name input:

	locTitle = cmds.text( label='Create a loc with name input:')

	locNameInput = cmds.textFieldGrp()

	locComment = cmds.text( label='name =\'input\' + \'_XXX_locPosition\'')	

	createLocBtn = cmds.button(label= 'Create Loc', command = partial(midleLoc,'Loc Created'))

	cmds.separator(height=5)
	#________
	createLocBtn = cmds.button(label= 'Create Multiple Locs', command = partial(multiLocs,'Multiples Locs Created'))

	cmds.separator(height=20)
	#________

	## Button to Create a joint chain from the selected locators parented in order:

	jntTitle = cmds.text( label='Create parented jnt chain from locs:')

	createJntBtn = cmds.button(label= 'Create jnt chain', command = jntChain)




if __name__ == '__main__':
	openUi()