
# ContainerGraph Tool

A Python-based tool for automatic detection and mitigation of vulnerabilities and misconfigurations for Docker containers. 


## Requirements

ContainerGraph runs as a Python script and uses the Neo4J graph database as a back-end storage, that you can run as a Docker container. ContainerGraph has been tested on MacOS and Ubuntu.

 - [Docker Installation](https://docs.docker.com/get-docker/)
 - [Python Installation](https://www.python.org/downloads/)

To run the ContainerGraph tool, it is also recommended to install a Python virtual environment, such as [Pipenv](https://pipenv.pypa.io/en/latest/install/). For example, by running `pip3 install pipenv`.


## How-to

To run the ContainerGraph tool, follow the next steps:

1. Clone this repository: `git clone https://github.com/fminna/ContainerGraph.git`

2. Move to the ContainerGraph directory `cd ContainerGraph`, and create a Python virtual environment: `pipenv shell` (or `python3 -m pipenv shell`)

3. Install Python requirements: `pip install -r requirements.txt`

4. Set the required environmental variables:

```bash
export NEO4J_ADDRESS=localhost
export NEO4J_PORT=7687
export NEO4J_USER=neo4j
export NEO4J_PWS=password
```

[How to make env variables permanent](https://www.cherryservers.com/blog/how-to-set-list-and-manage-linux-environment-variables).

5. Create the Docker volumes to persiste the data if the container is stopped or rebooted, and run the Neo4J Docker container:

```bash
docker volume create --name cdata
docker volume create --name cplugins
```

```bash
docker run \
    --name neo4jcontainergraph \
    --restart always \
    --publish=7474:7474 --publish=7687:7687 \
    --detach \
    --env NEO4J_AUTH=neo4j/password \
    --env NEO4J_PLUGINS='["graph-data-science"]' \
    --env server_default__listen__address="0.0.0.0" \
    --env server_default__advertised__address="0.0.0.0" \
    --env server_bolt_enabled="true" \
    --env server_bolt_listen__address="0.0.0.0:7687" \
    --env NEO4J_dbms_security_procedures_unrestricted=gds.* \
    --env NEO4J_dbms_security_procedures_allowlist=gds.* \
    --env dbms_memory_heap_max_size=5G \
    neo4j:5.5
```

Once the container is up and running, you can run cypher quieres to check that everything is working as expected. For example, you can connect to the Neo4J container with the following command (username:neo4j, password:password):

```bash
docker exec -it neo4jcontainergraph cypher-shell
```

Now, you can execute Neo4j quieres, for example:

```bash
neo4j@neo4j> MATCH (N) RETURN COUNT(N);
```

**If instead you use Neo4J Desktop, remember to apply the same options (e.g., install the graph-data-science, set the memory.heap.max.size to 5G, etc.) to the database settings.**

6. Finally, we can run the ContainerGraph tool, using the following command: `python main.py --help`

_Keep in mind that the first time you run the tool, it may take around 45 minutes to initialize all configurations and vulnerabilities into the Neo4J database._


## Usage Examples

Following some usage examples:

 - Execute a new privileged container: `python main.py --run docker run --name nginxpriv -it --rm -d --privileged nginx`

 - Analyze the container for misconfigurations and vulnerabilities: `python main.py --analyze`


## Interaction with the Neo4J Database

From your host machine, you can access the Neo4J browser interface to interact with the data stored in the database at the following address:

<http://localhost:7474/browser/>

The credentials to login in are the ones used to start the Neo4J container, by default user: `neo4j`, and password: `password`.

 - To query the database, check some [query examples](https://neo4j.com/developer/cypher/querying/).

 - To change the number of nodes displayed in the browser, check the [Neo4j documentation](https://neo4j.com/docs/browser-manual/current/operations/browser-settings/#adjust-in-browser).


## Issues and Bugs

For any issue and bug you encounter while using the tool, please open an issue on this repository.

