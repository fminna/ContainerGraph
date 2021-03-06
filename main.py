from build_image import build_image, retrieve_img_id
from build_container import build_container
from build_cont_Neo4j import cont_Neo4j_chart
from build_img_Neo4j import image_Neo4j_chart
from build_host_Neo4j import get_kernel_v
from remove_cont import data_remove_all, remove_container
from initialize_Neo4J import initialize_Neo4j_db, graph_info
from suggest_fix import analyze_single_deployment, analyze_all_deployment
import argparse
import os


parser = argparse.ArgumentParser(description="ContainerGraph - A tool to generate security charts (in XML and Neo4J) and detect drift of Docker containers.")
group = parser.add_mutually_exclusive_group(required=True)

group.add_argument("--add", metavar="<image_id>", help="add a new image")
group.add_argument("--run", action='append', nargs=argparse.REMAINDER, help="run a container")
group.add_argument("--remove", nargs=1, metavar="<container_id> OR <all>", help="remove and delete one container or all containers")
group.add_argument("--analyze", nargs=1, metavar="<container_id> OR <all>", help="analyze vulnerabilities/misconfigurations")

args = parser.parse_args()


# Define Neo4J Default address
NEO4J_ADDRESS = "localhost"


# Add a container image
def add_option(NEO4J_ADDRESS, img_id) :
    
    # Standardize the Image ID lenght to 7 chars.
    img_id = retrieve_img_id(img_id)
    
    # Build the Container Image
    img = build_image(img_id)

    # Generate Image Security Charts
    image_Neo4j_chart(NEO4J_ADDRESS, img)

    # Print graph info
    n_nodes, n_edges = graph_info(NEO4J_ADDRESS)
    print("Successfully added the image with ID " + img_id)
    print('Total: ' + str(n_nodes) + ' nodes and ' + str(n_edges) + ' relationships.\n')


# Run a new container
def run_option(NEO4J_ADDRESS, options) :

    # Get the current kernel version
    kernel_v = get_kernel_v(NEO4J_ADDRESS)

    # Build the Container 
    cont = build_container(options, kernel_v)

    # Eventually add the container image
    add_option(NEO4J_ADDRESS, cont.img_id)
    
    cont_Neo4j_chart(NEO4J_ADDRESS, cont) 

    # Print graph info
    n_nodes, n_edges = graph_info(NEO4J_ADDRESS)
    print("Successfully added the container with ID " + cont.cont_id)
    print('Total: ' + str(n_nodes) + ' nodes and ' + str(n_edges) + ' relationships.\n')


# Analyze all vulnerabilities/misconfigurations
def analyze_option(NEO4J_ADDRESS, option) :
    # Analyze all containers
    if option[0] == 'all' : 
        analyze_all_deployment(NEO4J_ADDRESS)
    # Analyze single container
    else :
        analyze_single_deployment(NEO4J_ADDRESS, option[0])
    

# Remove container/s and clean DB
def remove_option(NEO4J_ADDRESS, option) :
    # Remove all containers
    if option[0] == 'all' : 
        data_remove_all(NEO4J_ADDRESS)
    # Remove single container
    else :
        remove_container(NEO4J_ADDRESS, option[0])


def main() :

    if 'NEO4J_ADDRESS' in os.environ:
        global NEO4J_ADDRESS
        NEO4J_ADDRESS = os.environ.get('NEO4J_ADDRESS')

    # Eduroam
    # NEO4J_ADDRESS = ""

    if args.remove :
        remove_option(NEO4J_ADDRESS, args.remove)

    else :
        # First, make sure Neo4j is initialized
        initialize_Neo4j_db(NEO4J_ADDRESS)

        if args.add :
            add_option(NEO4J_ADDRESS, args.add)

        elif args.run :
            run_option(NEO4J_ADDRESS, args.run)

        elif args.analyze :
            analyze_option(NEO4J_ADDRESS, args.analyze)


if __name__ == "__main__" :
    main()

