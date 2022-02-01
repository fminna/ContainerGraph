import os
from parse_Dockerfile import parse_Dockerfile
import docker
import json


class Image:
    """
    Add comments
    """

    def __init__(self, img_id, repo, tag, t_created, img_size, df, sbom):
        self.img_id = img_id
        self.repo = repo
        self.tag = tag
        self.t_created = t_created
        self.img_size = img_size
        self.Dockerfile = df
        self.SBOM = sbom


def img_already_existing(img_id) :
    """
    Add comments
    """

    return False


def print_img_attr(img_id) : 
    """
    Given an image ID, it prints the image's attributes.

    Parameters
    ---------
    img_id: str
        Image ID (minimum 3 chars)

    Returns
    -------
    str:
        A corresponding Image object
    """
    client = connect_to_Docker()

    try:
        img = client.images.get(img_id)
        print(json.dumps(img.attrs, indent=1))

    # Raise an exception if the image doesn't exist
    except docker.errors.ImageNotFound :
        print("Image not found! Exiting...")
        exit(1)
    except docker.errors.APIError :
        print("Error while connecting to the Docker API! Exiting...")
        exit(1)


def reconstruct_Dockerfile(img_hst) :
    """ 
    Description

    Parameters
    ---------
    name: type
        Description

    Returns
    -------
    type:
        Description
    """

    # Create a Dockerfile file
    f = open("Dockerfile", "w+")

    # Iterate over the image commands and save them into the file
    for cmd in reversed(img_hst) :

        field = cmd.get("CreatedBy")
        if field != None : f.write(field[18:].lstrip() + "\n")
    
    f.close()


def generate_sbom(image_id) :
    """
    Given a container image ID, it generates a software bill of material (SBOM).

    Returns
    -------
    type: list of strings
        Returns the software packages within the image as a list of strings
    """
    
    sbom = []
    
    # Check if syft is installed

    # Run syft
    # syft <image_id> > <image_id>_sbom (save in )

    # Convert <image_id>_sbom to a table
    # | NAME | VERSION | TYPE

    # Convert the sbom table to a python dictionary
    # packages --> name, version, type

    # Store a json in GraphML

    # Remove the sbom file

    return sbom


def connect_to_Docker() : 
    """ 
    Connects to the Docker daemon running on the current host

    Returns
    -------
    Docker client:
        Returns a client configured from environment variables.
    """

    # Connect to the Docker daemon
    client = docker.from_env()
    return client


def build_one_image(img_id) :
    """ 
    Given an image ID, it returns an Image object containing all the information

    Parameters
    ---------
    img_id: str
        Image ID (minimum 3 chars)

    Returns
    -------
    type:
        Description
    """

    client = connect_to_Docker()

    try:
        img = client.images.get(img_id)

        # Retrieve repo and tag (only the first one)
        if img.tags :
            repo = img.tags[0].split(':')[0]
            tag = img.tags[0].split(':')[1]
        else :
            repo = "<none>"
            tag = "<none>"

        # When the image was created (on the host)
        t_created = img.attrs['Created'][:10]
        
        # Image size
        img_size = str(img.attrs['Size'])[:3] + 'MB'

        # Reconstruct the Dockerfile 
        reconstruct_Dockerfile(img.history())
        df = parse_Dockerfile(".")
        # For now, remove the Dockerfile
        # Alternatively, we can save all Dockerfiles in a folder
        os.remove("Dockerfile")

        # Build a SBOM of the image
        # The SBOM is saved as a list of software packages 
        sbom = generate_sbom(img_id)

        img = Image(img_id, repo, tag, t_created, img_size, df, sbom)
        return img

    # Raise an exception if the image doesn't exist
    except docker.errors.ImageNotFound :
        print("Image not found! Exiting...")
        exit(1)
    except docker.errors.APIError :
        print("Error while connecting to the Docker API! Exiting...")
        exit(1)


def build_images(img_id_list) :
    """ 
    Given a list of image IDs, it builds and returns corresponding 
    Image objects.

    Parameters
    ---------
    img_id_list: list
        List of Image IDs

    Returns
    -------
    list:
        A list of Image objects
    """

    img_list = []

    for img_id in img_id_list : 
        img_list.append(build_one_image(img_id))

    return img_list
