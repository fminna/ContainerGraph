import os
import docker
import json


#
#
#
# Docker SBOM
#
# https://www.docker.com/blog/announcing-docker-sbom-a-step-towards-more-visibility-into-docker-images/
#
#


class Image :
    """  brief title.
    
    Arguments:
    arg1 - desc
    arg2 - desc

    Description:
    blablabla
    """

    def __init__(self, img_id, name, repo, tag, t_created, img_size, sbom):
        self.img_id = img_id
        self.name = name
        self.repo = repo
        self.tag = tag
        self.t_created = t_created
        self.img_size = img_size
        self.SBOM = sbom


def retrieve_img_id(img_id) :
    """  brief title.
    
    Arguments:
    arg1 - desc
    arg2 - desc

    Description:
    blablabla
    """

    client = connect_to_Docker()

    try:
        img = client.images.get(img_id)
        return img.short_id[7:]

    except docker.errors.ImageNotFound as error:
        print(error)
        exit(1)
    except docker.errors.APIError as error:
        print(error)
        exit(1)


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
    return docker.from_env()


def build_image(img_id) :
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

        img_id = img.short_id[7:]
        name = img.tags[0]

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

        # Build a SBOM of the image
        # The SBOM is saved as a list of software packages 
        sbom = generate_sbom(img_id)

        img = Image(img_id, name, repo, tag, t_created, img_size, sbom)
        return img

    # Raise an exception if the image doesn't exist
    except docker.errors.ImageNotFound :
        print("Image not found! Exiting...")
        exit(1)
    except docker.errors.APIError :
        print("Error while connecting to the Docker API! Exiting...")
        exit(1)

