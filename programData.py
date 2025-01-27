class ProgramData:

    def getThreshold():
        threshold = [254, 254, 254]
        return threshold
    def getKernelSize():
        kernelSize = 1
        return kernelSize
    def getMonochromeThreshold():
        threshold = 127
        return threshold
    def getMaskSize():
        maskSize = 2
        return maskSize
    def getPath():
        path = "picsBlack/img29.png"
        #path = "pictures/imgEx.png" 
        #path = "pictures/Untitled.png"
        return path
    


import os
import shutil

def clear_folder(folder_path):
    # Check if the folder exists
    if not os.path.exists(folder_path):
        raise ValueError(f"The folder '{folder_path}' does not exist.")
    
    # Iterate over all items in the folder
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.islink(file_path):  # Handle symbolic links
                os.unlink(file_path)
            elif os.path.isdir(file_path):  # Handle directories
                shutil.rmtree(file_path)
            else:  # Handle files
                os.unlink(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")

