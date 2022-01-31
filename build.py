import shutil, zipfile, os, fileinput, fire, sys
from pathlib import Path

def type6(templateVersion=0.0, modelVersions=0.0, cleanup='y'):
  """
    Creates a set of .xpt archives, inside a single .xpta model archive, which can be installed into eXact's Online Editor.
    :param templateVersion: The version of the templates and all models within it (e.g. ELFH_Session version and ELFH_Radio version)
    :param cleanup: default is 'y', to to remove all the copied files and folders that are created during the build process.  Set to 'n' if you want to debug an issue with the build script.
    :return: An .xpta file that can be installed in eXact Packager
  """
  models = [  {   'name': 'ELFH_ANIMATION', 
                    'sharedStyles': ['htmlTransformations.xsl', 'richTextEditor.xsl'],
                    'sharedCommon': []
                },
                {   'name': 'ELFH_Assessment', 
                    'sharedStyles': ['htmlTransformations.xsl', 'richTextEditor.xsl'],
                    'sharedCommon': []
                },
                {   'name': 'ELFH_Check', 
                    'sharedStyles': ['htmlTransformations.xsl', 'richTextEditor.xsl'],
                    'sharedCommon': []
                },
                {   'name': 'ELFH_Free', 
                    'sharedStyles': ['htmlTransformations.xsl', 'richTextEditor.xsl'],
                    'sharedCommon': []
                },
                {   'name': 'ELFH_IMG_STACKER', 
                    'sharedStyles': ['htmlTransformations.xsl', 'richTextEditor.xsl'],
                    'sharedCommon': []
                },
                {   'name': 'ELFH_JS_DDP', 
                    'sharedStyles': ['htmlTransformations.xsl', 'richTextEditor.xsl'],
                    'sharedCommon': []
                },
                {   'name': 'ELFH_JS_INFO_HS', 
                   'sharedStyles': ['htmlTransformations.xsl', 'richTextEditor.xsl'],
                   'sharedCommon': []
                },
                {   'name': 'ELFH_JS_QUES_HS', 
                    'sharedStyles': ['htmlTransformations.xsl', 'richTextEditor.xsl'],
                    'sharedCommon': []
                },
                {   'name': 'ELFH_MRB', 
                    'sharedStyles': ['htmlTransformations.xsl', 'richTextEditor.xsl'],
                    'sharedCommon': []
                },
                {   'name': 'ELFH_Multi', 
                    'sharedStyles': [],
                    'sharedCommon': []
                },
                {   'name': 'ELFH_Pairs', 
                    'sharedStyles': ['htmlTransformations.xsl', 'richTextEditor.xsl'],
                    'sharedCommon': []
                },
                {   'name': 'ELFH_Question_Bank', 
                    'sharedStyles': [],
                    'sharedCommon': []
                },
                {   'name': 'ELFH_Radio', 
                    'sharedStyles': ['htmlTransformations.xsl', 'richTextEditor.xsl'],
                    'sharedCommon': []
                },
                {   'name': 'ELFH_Session', 
                    'sharedStyles': ['htmlTransformations.xsl', 'richTextEditor.xsl'],
                    'sharedCommon': []
                },
                {   'name': 'ELFH_Sort', 
                    'sharedStyles': ['htmlTransformations.xsl', 'richTextEditor.xsl'],
                    'sharedCommon': []
                },
                {   'name': 'ELFH_Sort_Order', 
                    'sharedStyles': ['htmlTransformations.xsl', 'richTextEditor.xsl'],
                    'sharedCommon': []
                },
                {   'name': 'ELFH_STREAM_VIDEO', 
                    'sharedStyles': [],
                    'sharedCommon': []
                },
                {   'name': 'ELFH_Tab', 
                    'sharedStyles': ['htmlTransformations.xsl', 'richTextEditor.xsl'],
                    'sharedCommon': []
                },
                {   'name': 'ELFH_TF', 
                    'sharedStyles': ['htmlTransformations.xsl', 'richTextEditor.xsl'],
                    'sharedCommon': []
                }
           ]     

#    modelFolders = [    'ELFH_Session', 
#                        'ELFH_Free']


  if templateVersion == 0.0:
      print('Specify the template version (e.g. 6.1):')
      templateVersion = input()

  modelVersions = templateVersion

  #if modelVersions == 0.0:
  #    print('Specify the version for the models (e.g. 6.1):')
  #    modelVersions = input()

  try:
      val = float(templateVersion)
      val = float(modelVersions)
  except ValueError:
      print("Error!  Template and model versions must be a floating point number, e.g. 1.0")
      sys.exit()    

  cwd = Path.cwd()

  distFolder = 'dist'
  xptaFilename = 'eXact-elfh-templates'
  subLOSearchStr = '<item type="lo" version=""'
  subLOReplaceStr = '<item type="lo" version="' + str(modelVersions) + '"'
  xptVersionSearchStr = '<template version=""'
  xptVersionReplaceStr = '<template version="' + str(modelVersions) + '"'
  rootVersionReplaceStr = '<template version="' + str(templateVersion) + '"'

  if Path.exists(cwd / distFolder):
      shutil.rmtree(cwd / distFolder)

  os.mkdir(cwd / distFolder)

  buildFolder = Path.absolute(cwd / 'dist')

  print('Copying models ...')

  templateZip = zipfile.ZipFile('dist\\' + xptaFilename, 'w', zipfile.ZIP_DEFLATED)

  for model in models:

      modelName = model["name"]
      modelPath = Path.absolute(buildFolder / modelName)

      # copy model code into build folder
      shutil.copytree(cwd / modelName, buildFolder / modelName)
      
      if not Path.exists(buildFolder / modelName / "styles"):
          os.mkdir(buildFolder / modelName / "styles")

      if not Path.exists(buildFolder / modelName / "common"):
          os.mkdir(buildFolder / modelName / "common")

      for styleFile in model["sharedStyles"]:
          shutil.copyfile(cwd / "shared/styles" / styleFile, buildFolder / modelName / "styles" / styleFile)

      # add version numbers to the LO's configuration files
      with fileinput.FileInput(Path.absolute(buildFolder / modelName / 'lomodel.xml'), inplace=True) as file:
          for line in file:
              newLine = line.replace(subLOSearchStr, subLOReplaceStr) # add sub lo version number
              if model == 'ELFH_Session':
                  newLine = newLine.replace(xptVersionSearchStr, rootVersionReplaceStr) # if this is the root LO, add the template version number to the top of the lomodel.xml
              else:
                  newLine = newLine.replace(xptVersionSearchStr, xptVersionReplaceStr) # if this a sub lo, add the lo's version number to the top of the file

              print(newLine, end='') # write the modified line to the file   
      
      # zip the model up into an xpt
      shutil.make_archive(buildFolder / modelName, 'zip', buildFolder / modelName)
      xptPath = str(modelName)+'.xpt'
      os.rename(str(buildFolder / modelName)+'.zip', str(buildFolder) + '\\' + xptPath )

      # put the xpt into the template zip file
      templateZip.write(  str(buildFolder) + '\\' + xptPath, xptPath  )

      # clean up, delete the build folder model, it's no longer needed
      if cleanup != 'n':
          shutil.rmtree(buildFolder / modelName)
          os.remove(str(buildFolder) + '\\' + xptPath)
          

      print(str(model["name"]) + ' built')


  templateZip.close()

  os.rename(str(buildFolder)+'\\' + xptaFilename, str(buildFolder) + '\\' + xptaFilename + '-v' + str(templateVersion) + '.xpta')

  print('Build Complete')

def type4(templateVersion=0.0, cleanup='y'):
  """
  Creates a set of .xpt archives, inside a single .xpta model archive, which can be installed into eXact Packager.
  :param templateVersion: The version of the templates (ELFH_LO version)
  :param cleanup: default is 'y', to to remove all the copied files and folders that are created during the build process.  Set to 'n' if you want to debug an issue with the build script.
  :return: An .xpta file that can be installed in eXact Packager
  """

  if templateVersion == 0.0:
      print('Specify the template version (e.g. 4.11):')
      templateVersion = input()

  modelVersions = templateVersion

#    if modelVersions == 0.0:
#        print('Specify the version for the models (e.g. 1.3):')
#        modelVersions = input()

  try:
      val = float(templateVersion)
      val = float(modelVersions)
  except ValueError:
      print("Error!  Template and model versions must be a floating point number, e.g. 1.0")
      sys.exit()    

  cwd = Path.cwd()

  distFolder = 'dist'
  xptaFilename = 'eXact-elfh-templates'
  subLOSearchStr = '<item type="lo" version=""'
  subLOReplaceStr = '<item type="lo" version="' + str(modelVersions) + '"'
  xptVersionSearchStr = '<template version=""'
  xptVersionReplaceStr = '<template version="' + str(modelVersions) + '"'
  rootVersionReplaceStr = '<template version="' + str(templateVersion) + '"'

  if Path.exists(cwd / distFolder):
      shutil.rmtree(cwd / distFolder)

  os.mkdir(cwd / distFolder)

  buildFolder = Path.absolute(cwd / 'dist')

  modelFolders = [    'ELFH_ANIMATION',
                      'ELFH_Assessment',
                      'ELFH_Check',
                      'ELFH_Free',
                      'ELFH_IMG_STACKER',
                      'ELFH_JS_DDP',
                      'ELFH_JS_INFO_HS',
                      'ELFH_JS_QUES_HS',
                      'ELFH_LO',
                      'ELFH_Page',
                      'ELFH_MRB',
                      'ELFH_Multi',
                      'ELFH_Pairs',
                      'ELFH_Question_Bank',
                      'ELFH_Radio',
                      'ELFH_Sort',
                      'ELFH_Sort_Order',
                      'ELFH_STREAM_VIDEO',
                      'ELFH_Tab',
                      'ELFH_TF'
                  ]

  #modelFolders = [  'ELFH_LO' ]

  print('Copying models ...')

  templateZip = zipfile.ZipFile('dist\\' + xptaFilename, 'w', zipfile.ZIP_DEFLATED)

  for model in modelFolders:

      modelPath = Path.absolute(buildFolder / model)

      # copy model code into build folder and include common and styles folders
      shutil.copytree(cwd / model, buildFolder / model)
      shutil.copytree(cwd / 'common', modelPath / 'common', dirs_exist_ok=True)
      shutil.copytree(cwd / 'styles', modelPath / 'styles', dirs_exist_ok=True)

      # add version numbers to the LO's configuration files
      with fileinput.FileInput(Path.absolute(buildFolder / model / 'lomodel.xml'), inplace=True) as file:
          for line in file:
              newLine = line.replace(subLOSearchStr, subLOReplaceStr) # add sub lo version number
              if model == 'ELFH_LO':
                  newLine = newLine.replace(xptVersionSearchStr, rootVersionReplaceStr) # if this is the root LO, add the template version number to the top of the lomodel.xml
              else:
                  newLine = newLine.replace(xptVersionSearchStr, xptVersionReplaceStr) # if this a sub lo, add the lo's version number to the top of the file

              print(newLine, end='') # write the modified line to the file   
      
      # zip the model up into an xpt
      shutil.make_archive(buildFolder / model, 'zip', buildFolder / model)
      xptPath = str(model)+'.xpt'
      os.rename(str(buildFolder / model)+'.zip', str(buildFolder) + '\\' + xptPath )

      # put the xpt into the template zip file
      templateZip.write(  str(buildFolder) + '\\' + xptPath, xptPath  )

      # clean up, delete the build folder model, it's no longer needed
      if cleanup != 'n':
          shutil.rmtree(buildFolder / model)
          os.remove(str(buildFolder) + '\\' + xptPath)


      print(str(model) + ' built')


  templateZip.close()

  os.rename(str(buildFolder)+'\\' + xptaFilename, str(buildFolder) + '\\' + xptaFilename + '-v' + str(templateVersion) + '.xpta')

  print('Build Complete')

if __name__ == "__main__":
  fire.Fire({
    'type4': type4,
    'type6': type6,
  })