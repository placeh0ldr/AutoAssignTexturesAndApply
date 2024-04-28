import maya.cmds as cmds
import os


textureSource = "sourceimages\\"

def attemptCreateMaterial():
    #Get the name of the selected mesh

    meshName = cmds.ls(selection=True)
    
    #If no mesh is selected
    if not meshName:
        cmds.confirmDialog(message="No object selected")
        buildUI()
    elif cmds.textField('DefinedName', query=True,text=True) == '': #If there's no name
        cmds.confirmDialog(message="Material has no name")
        buildUI()  
    else:
        try: 
            createMaterial()
        except TypeError:
            cmds.confirmDialog(message="No texture types selected")
            buildUI()
            

def createMaterial():
    global dirPath,material, shader, searchName, filePath, fileNames, textureTypes, diffuseDone, roughnessDone, metalDone, normalDone, subsurfaceDone, displacementDone
    
    meshName = cmds.ls(selection=True)
    #opens a window to find the file where the textures are located
    dirPath = cmds.fileDialog2(fileMode=3, caption="Select the textures folder")[0] + "\\"
    fileNames = [f for f in os.listdir(dirPath) if os.path.isfile(os.path.join(dirPath, f))]
    print(fileNames)
    
    textureTypes = ["_Diffuse", "_Roughness", "_Metalness", "_Subsurface", "_Displacement", "_Normal"]
    
    
    #Set up names for nodes
    searchName = cmds.textField('DefinedName', query=True,text=True)
    matName = cmds.textField('DefinedName', query=True,text=True) + '_material'
    shaderName = cmds.textField('DefinedName', query=True,text=True) + '_shader'

    
    #Creating the materials based on what the user has set
    if not cmds.objExists(matName):
        if cmds.radioButton(ArnoldChecked, query = True,select =True): #If the arnold option is selected, an aiStandardSurface is created
            material = cmds.shadingNode('aiStandardSurface', name=matName, asShader=True)
           
            
        if cmds.radioButton(VrayChecked, query = True,select =True): #If the vray option is selected, a vrayMaterial is created
             material = cmds.shadingNode('VRayMtl', name=matName, asShader=True)

            
        if cmds.radioButton(LambertChecked, query = True,select =True): #If the lambert option is selected, a lambert material is created
            material = cmds.shadingNode('lambert', name=matName, asShader=True)
            
    #Creates the shader and connects it to the material           
    shader = cmds.shadingNode('shadingEngine', name = shaderName, asUtility=True)
    shader = cmds.sets(renderable=True, noSurfaceShader=True, empty=True)  
    cmds.connectAttr(material +'.outColor', shader +'.surfaceShader')
    
    diffuseDone = roughnessDone = metalDone = normalDone = subsurfaceDone = displacementDone = 0
    
    #Starts setting the text files
    SetTextureFile(diffuseDone, roughnessDone, metalDone, normalDone, subsurfaceDone, displacementDone)
     
    #Assign material
    cmds.select(meshName, replace=True)
    cmds.hyperShade(assign = material)

                
                
def SetTextureFile(diffuseDone, roughnessDone, metalDone, normalDone, subsurfaceDone, displacementDone):
    #Looks through all files in the selected folder
    for f in range(len(fileNames)):
        for t in range(len(textureTypes)):
            if textureTypes[t] in fileNames[f]:
                filePath = fileNames[f]
                textureType = textureTypes[t]
                
                #If the file name ends in _Diffuse
                if textureType == "_Diffuse" and cmds.checkBox('Diffuse', query = True, value=True):
                    if diffuseDone == 0:
                        textureNode = cmds.shadingNode('file', name = 'DiffuseTexture', asTexture=True)
                        #Changes the connection name based on what mat type is selected
                        #Creates a texturenode and connects it to the material
                        if cmds.radioButton(ArnoldChecked, query = True,select =True): 
                            cmds.connectAttr(textureNode + '.outColor', material + '.baseColor')
                            diffuseDone = 1
                        elif cmds.radioButton(VrayChecked, query = True,select =True):
                            cmds.connectAttr(textureNode + '.outColor', material + '.diffuseColor')
                            diffuseDone = 1
                        elif cmds.radioButton(LambertChecked, query = True,select =True):
                            cmds.connectAttr(textureNode + '.outColor', material + '.color')
                            diffuseDone = 1
                        #Sets the values associated with colorSpace etc.
                        cmds.setAttr(textureNode + ".colorSpace", "sRGB", type='string')
                        cmds.setAttr(textureNode+'.alphaIsLuminance',0)
                        twoDTexture = cmds.shadingNode('place2dTexture', asUtility=True)
                        cmds.connectAttr(twoDTexture + '.outUV', textureNode + '.uvCoord') 
                        textureFile = dirPath + filePath
                        #Load the diffuse texture into the texturenode
                        cmds.setAttr(textureNode + '.fileTextureName', textureFile, type="string")
                        print(textureFile + ' loaded into diffuse')
                        diffuseDone = 1
                        
                #If the file name ends in _Roughness    
                if textureType == "_Roughness" and cmds.checkBox('Roughness', query = True, value=True):
                    if roughnessDone == 0:
                        textureNode = cmds.shadingNode('file', name = 'RoughnessTexture', asTexture=True)
                        #Changes the connection name based on what mat type is selected
                        #Creates a texturenode and connects it to the material
                        if cmds.radioButton(ArnoldChecked, query = True,select =True): 
                            cmds.connectAttr(textureNode + '.outAlpha', material + '.specularRoughness') 
                            roughnessDone = 1 
                        elif cmds.radioButton(VrayChecked, query = True,select =True):
                            cmds.connectAttr(textureNode + '.outAlpha', material + '.reflectionGlossiness')
                            cmds.setAttr(textureNode + ".useRoughness",1)
                            roughnessDone = 1 
                        #Sets the values associated with colorSpace etc.    
                        cmds.setAttr(textureNode + ".colorSpace", "Raw", type='string')
                        cmds.setAttr(textureNode+'.alphaIsLuminance',1)
                        twoDTexture = cmds.shadingNode('place2dTexture', asUtility=True)
                        cmds.connectAttr(twoDTexture + '.outUV', textureNode + '.uvCoord')
                        textureFile = dirPath + filePath
                        #Load the diffuse texture into the texturenode
                        cmds.setAttr(textureNode + '.fileTextureName', textureFile, type="string")
                        print(textureFile + ' loaded into roughness')
                        roughnessDone = 1
                
                #If the file name ends in _Metal  
                if textureType == "_Metal" and cmds.checkBox('Metal', query = True, value=True):
                    if metalDone == 0:
                        textureFile = dirPath + filePath
                        #Creates a texturenode and connects it to the material
                        textureNode = cmds.shadingNode('file', name = 'MetalTexture', asTexture=True)
                        cmds.connectAttr(textureNode + '.outAlpha', material + '.metalness')
                        #Sets the values associated with colorSpace etc
                        cmds.setAttr(textureNode + ".colorSpace", "Raw", type='string')
                        cmds.setAttr(textureNode+'.alphaIsLuminance',1)
                        twoDTexture = cmds.shadingNode('place2dTexture', asUtility=True)
                        cmds.connectAttr(twoDTexture + '.outUV', textureNode + '.uvCoord')

                        #Load the diffuse texture into the texturenode
                        cmds.setAttr(textureNode + '.fileTextureName', textureFile, type="string")
                        print(textureFile + ' loaded into metal')
                        metalDone = 1
                    
                if textureType == "_Subsurface" and cmds.checkBox('Subsurface', query = True, value=True):
                    if subsurfaceDone == 0:
                        textureFile = dirPath + filePath
                        #Creates a texturenode and connects it to the material
                        textureNode = cmds.shadingNode('file', name = 'SubsurfaceTexture', asTexture=True)
                        cmds.connectAttr(textureNode + '.outAlpha', material + '.subsurface')
                        twoDTexture = cmds.shadingNode('place2dTexture', asUtility=True)
                        cmds.connectAttr(twoDTexture + '.outUV', textureNode + '.uvCoord')
                        #Load the diffuse texture into the texturenode
                        cmds.setAttr(textureNode + '.fileTextureName', textureFile, type="string")
                        print(textureFile + ' loaded into subsurface')
                        subsurfaceDone = 1
                
                if textureType == "_Displacement" and cmds.checkBox('Displacement', query = True, value=True):
                    if displacementDone == 0:
                        #Creates a texturenode and connects it to the material
                        textureNode = cmds.shadingNode('file', name = 'DisplacementTexture', asTexture=True)
                        displShade = cmds.shadingNode('displacementShader', asUtility=True)
                        cmds.connectAttr(textureNode + '.outColor.outColorR', displShade + '.displacement')
                        cmds.connectAttr(displShade + '.displacement', shader + '.displacementShader')
                        twoDTexture = cmds.shadingNode('place2dTexture', asUtility=True)
                        cmds.connectAttr(twoDTexture + '.outUV', textureNode + '.uvCoord')
                        textureFile = dirPath + filePath
                        #Load the diffuse texture into the texturenode
                        cmds.setAttr(textureNode + '.fileTextureName', textureFile, type="string")
                        print(textureFile + ' loaded into displacement')
                        displacementDone = 1
                    
                if textureType == "_Normal" and cmds.checkBox('Normal', query = True, value=True):
                    if normalDone == 0:
                        #Changes the connection name based on what mat type is selected
                        #Creates a texturenode and connects it to the material
                        textureNode = cmds.shadingNode('file', name = 'NormalTexture', asTexture=True)
                        if cmds.radioButton(ArnoldChecked, query = True,select =True):
                            normalNode = cmds.shadingNode('aiNormalMap', name = 'aiNormalMap', asTexture=True)
                            cmds.connectAttr(textureNode + '.outColor', normalNode + '.input')
                            cmds.connectAttr(normalNode + '.outValue', material + '.normalCamera')
                            roughnessDone = 1 
                        
                        elif cmds.radioButton(VrayChecked, query = True,select =True):
                            cmds.connectAttr(textureNode + '.outColor', normalNode + '.bumpMap')
                            roughnessDone = 1 
                        #Sets the values associated with colorSpace etc
                        cmds.setAttr(textureNode + ".colorSpace", "Raw", type='string')
                        cmds.setAttr(textureNode+'.alphaIsLuminance',0)
                        twoDTexture = cmds.shadingNode('place2dTexture', asUtility=True)
                        cmds.connectAttr(twoDTexture + '.outUV', textureNode + '.uvCoord')
                        textureFile = dirPath + filePath
                        #Load the diffuse texture into the texturenode
                        cmds.setAttr(textureNode + '.fileTextureName', textureFile, type="string")
                        print(textureFile + ' loaded into normal')
                        normalDone = 1
                  
def ArnoldOptions():
    #Enables all options
    cmds.checkBox(DiffuseChecked,edit=True, value=False, enable=True)
    cmds.checkBox(RoughnessChecked,edit=True, value=False, enable=True)
    cmds.checkBox(MetalChecked,edit=True, value=False, enable=True)
    cmds.checkBox(SubsurfaceChecked,edit=True, value=False, enable=True)
    cmds.checkBox(NormalChecked,edit=True, value=False, enable=True)
    cmds.checkBox(DisplacementChecked,edit=True, value=False, enable=True)
    
def VrayOptions():
    #Enables all options
    cmds.checkBox(DiffuseChecked,edit=True, value=False, enable=True)
    cmds.checkBox(MetalChecked,edit=True, value=False, enable=True)
    cmds.checkBox(RoughnessChecked,edit=True, value=False, enable=True)
    cmds.checkBox(NormalChecked,edit=True, value=False, enable=True)
    cmds.checkBox(DisplacementChecked,edit=True, value=False, enable=True)
    cmds.checkBox(SubsurfaceChecked,edit=True, value=False, enable=True)

def lambertOptions():
    #Enables diffuse and displacement
    cmds.checkBox(DiffuseChecked,edit=True, value=False, enable=True)
    cmds.checkBox(DisplacementChecked,edit=True, value=False, enable=True)
    
    #Disables all other options
    cmds.checkBox(RoughnessChecked,edit=True, value=False, enable=False)
    cmds.checkBox(MetalChecked,edit=True, value=False, enable=False)
    cmds.checkBox(SubsurfaceChecked,edit=True, value=False, enable=False)
    cmds.checkBox(NormalChecked,edit=True, value=False, enable=False)


def HowToUseWindow(self):
    
    if (cmds.window("HowToUse", exists=True)):
        cmds.deleteUI("HowToUse")
    #Sets up text explaining how to use the program
    HowWindow = cmds.window("HowToUse", title="How To Use", widthHeight = (250,100))
    
    cmds.columnLayout(adjustableColumn=True)
    cmds.text(label='1.Select the material type', align='left')
    cmds.separator(height=20)
    cmds.text(label='2.Type in your material name', align='left')
    cmds.separator(height=20)
    cmds.text(label='3.Select the types of textures you want to use', align='left')
    cmds.separator(height=20)
    cmds.text(label='4.Select the folder location of the textures', align='left')
    cmds.separator(height=20)
    cmds.text(label='IMPORTANT: Make sure you files are named correctly', align='left')
    cmds.text(label='(See About > Name Guide for details)', align='left')
    
    #Opens how to use window
    cmds.showWindow(HowWindow)

def NameGuideWindow(self):
    if (cmds.window("NameGuide", exists=True)):
        cmds.deleteUI("NameGuide")
    #sets up texts explain naming scheme
    NameGuide = cmds.window("NameGuide", title="Name Guide",widthHeight = (250,100))
    
    cmds.columnLayout(adjustableColumn=True)
    cmds.text(label='To make sure your textures are applied correctly, add these to the end of your textures', align='left')
    cmds.text(label='Base Color/Diffuse = "File Name" + "_Diffuse"', align='left')
    cmds.text(label='Roughness = "File Name" + "_Roughness"', align='left')
    cmds.text(label='Metal = "File Name" + "_Metalness"', align='left')
    cmds.text(label='Subsurface = "File Name" + "_Subsurface"', align='left')
    cmds.text(label='Displacement = "File Name" + "_Displacement"', align='left')
    cmds.text(label='Normal = "File Name" + "_Normal"', align='left')
    #creates window
    cmds.showWindow(NameGuide)
            
def buildUI():
    global ArnoldChecked, VrayChecked, LambertChecked, DiffuseChecked, RoughnessChecked, MetalChecked, SubsurfaceChecked, NormalChecked, DisplacementChecked
    if (cmds.window("MaterialCreate", exists=True)):
        cmds.deleteUI("MaterialCreate")
        
    #Create Layout
    winName = cmds.window("MaterialCreate", title="Material Create", widthHeight = (300, 200))
    cmds.columnLayout(adjustableColumn=True)
    
    #Sets up about menu
    menuBarLayout = cmds.menuBarLayout()
    cmds.menu( label='About' )
    cmds.menuItem(label='How to use', command= HowToUseWindow)
    cmds.menuItem(label='Name Guide', command= NameGuideWindow)

    #Create Checkboxes
    cmds.radioCollection()
    ArnoldChecked = cmds.radioButton( label='Arnold', select=True, changeCommand='ArnoldOptions()')
    VrayChecked = cmds.radioButton( label='Vray', changeCommand='VrayOptions()')
    LambertChecked = cmds.radioButton( label='Lambert', changeCommand='lambertOptions()')
    cmds.separator(height=20)    
    
    
    #Material Name + Create
    cmds.text( label='Material Name' )
    cmds.separator(height=2)
    cmds.textField('DefinedName',width =250)
    cmds.separator(height=20)
    

    #Texture Types
    DiffuseChecked = cmds.checkBox('Diffuse', label="Diffuse", value=False, enable=True)
    RoughnessChecked = cmds.checkBox('Roughness', label="Roughness", value=False, enable=True)
    MetalChecked = cmds.checkBox('Metal', label="Metal", value=False, enable=True)
    SubsurfaceChecked = cmds.checkBox('Subsurface', label="Subsurface", value=False, enable=True)
    NormalChecked = cmds.checkBox('Normal', label="Normal", value=False, enable=True)
    DisplacementChecked = cmds.checkBox('Displacement', label="Displacement", value=False, enable=True)
    cmds.separator(height=20)
    
    
    #Create Material Button
    createMat = cmds.button(label="Create Material and Apply", command="attemptCreateMaterial()")
    
    
    #Define window
    cmds.showWindow(winName)
    cmds.window(winName, e=True, width=350, height=350)
    return
  
buildUI()
