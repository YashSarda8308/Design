import pickle
class Material:
    '''
    To handle Material and their properties
    '''
    '''
    :material_dict -> To store the object of the material.
    '''
    material_dict = {}
    def __init__(self,name:str,Syt:float,Sys:float,Syc:float):
        '''
        Create the object of Material of following parameters and add it to material_dict Dictianory.

        :name -> (str) Name of the Material in string.
        :Syt -> (float) Shear Strength of the Material in Newton (N).
        :Sys ->(float) Shear Stress of the Material in Newton.
        :Syc ->(float) Compressive Stress of the Material.
        '''
        self.ShearStrength = Syt
        self.ShearStress = Sys
        self.CompressiveStress = Syc
        self.MaterialName = name
        Material.material_dict[self.MaterialName] = {"Syt":self.ShearStrength,"Syc": self.CompressiveStress,"Sys":self.ShearStress}
        self.createFile()

    @classmethod
    def loadFile(cls):
        '''
        It is a Class Method to load the objects from file or deserialize the Material object saved in Json file.
        :raise Exception if file is not found
        '''
        try:
            #Material.material_dict.update(Material.loadFile())
            f = open("material.txt",'r')
            Material.material_dict.update(pickle.loads(f))
            print("Material loads succefull")
        except Exception as e:
            print("Material load unsuccefull -> ",e)
        finally:
            f.close()


    def createFile(self):
        ''' It first see wheather the material file is present or not and then if not present creates file and 
        add or dump the material_dict in material file'''
        try:
            f = open("material.txt",'a')
            print(type(pickle.dumps(Material.material_dict)))
            f.write(pickle.dumps(Material.material_dict))
            print("Material dict dumped")
            return True
        except Exception as e:
            print(e);return False
        finally:
            f.close()

    @classmethod
    def printMaterials(cls):
        '''It is classMethod to print the material available in specific way'''
        
        for i in Material.material_dict:
            print(i,Material.material_dict[i])

Steel = Material("Steel","240","260","120")
# Aluminium = Material("Aluminium",150,150,240)
# Steel = Material("Iron+CO2",250,520,320)
print(Material.loadFile())
# Material.material_dict = Material.loadFile()
# Material.printMaterials()

