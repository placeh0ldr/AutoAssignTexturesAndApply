This code will create an Arnold/Vray/Lambert material (Based on user selection) and assign textures from the selected folder to that material, then apply it to a selected model
NOTE: The Vray option will not work if the Vray plugin is not installed

Installation:
This can be loaded into Maya's script editor and run from there 
OR
Create a new item on a maya shelf -> Set the command language to Python -> Copy and paste the code into the text box -> Run the code by clicking the icon in the shelf

How to use:
1.Select the object you want to apply the material to
2.Select the material type
3.Type in your material name
4.Select the types of textures you want to use
5.Select the folder location of the textures
6.The material made using the textures will be applied to the selected model


IMPORTANT: Make sure you files are named correctly according to the name guide:
Add these to the end of your file names
Base Color/Diffuse = "File Name" + "_Diffuse"
Roughness = "File Name" + "_Roughness"
Metal = "File Name" + "_Metalness"
Subsurface = "File Name" + "_Subsurface"
Displacement/Bump = "File Name" + "_Displacement"
Normal = "File Name" + "_Normal"
