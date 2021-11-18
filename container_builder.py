from dockerfile_parser import build_Dockerfile
import docker

from permission_taxonomy import Permissions


class Container:

    def __init__(self, ID, Dockerfile, fs, permissions):
        self.ID = ID
        self.Dockerfile = Dockerfile # other Class
        self.fs = fs # uri
        self.permissions = permissions # other Class


# Connect to the Docker daemon
client = docker.from_env()


# Ask the user to provide an image ID
def get_Image_ID():

    try:
        #Image_ID = input("Insert Image ID: ")
        Image_ID = "ea335eea17ab" # ONLY FOR TESTING

        aux = client.images.get(Image_ID)
        return aux, Image_ID

    # Raise an exception if the image doesn't exist
    except docker.errors.ImageNotFound :
        print("Image not found! Exiting...")
        exit(1)
    except docker.errors.APIError :
        print("Image not found! Exiting...")
        exit(1)


def reconstruct_Dockerfile(img_hst) :

    # Create a Dockerfile file
    f = open("Dockerfile", "w+")

    # Iterate over the image commands and save them into the file
    for cmd in reversed(img_hst) :

        field = cmd.get("CreatedBy")
        if field != None : f.write(field[18:].lstrip() + "\n")
    
    # Close the file
    f.close()


def build_Container():

    # Get image
    img, img_id = get_Image_ID()

    ### TO TRY ###
    # name = client.images.list(img_id)
    
    try:

        # Build Dockerfile
        img_hst = img.history()

        # Reconstruct the Dockerfile and save it to disk
        reconstruct_Dockerfile(img_hst)

        # Parse Dockerfile
        df = build_Dockerfile()
        # print(df.EXPOSE)

        # Add container filesystem location
        fs = "abc/def"

        # Add container's permissions
        
        
        
        
        perm = ""

        # Build the container
        aux = Container(img_id, df, fs, perm)
        return aux

    except docker.errors.APIError :
        print("Error while retrieving the image history! Exiting...")
        exit(1)







# build_Container()



