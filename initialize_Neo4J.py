from neo4j import GraphDatabase
from build_infrastructure import get_Infrastructure
from build_host_Neo4j import host_Neo4j
from init_Neo4j import init_Neo4j
import json


def connect_to_neo4j(uri, user, password) :
    return GraphDatabase.driver(uri, auth=(user, password))


def graph_info(NEO4J_ADDRESS) :
    """  brief title.
    
    Arguments:
    arg1 - desc
    arg2 - desc

    Description:
    blablabla
    """

    driver = connect_to_neo4j("bolt://" + NEO4J_ADDRESS + ":7687", "neo4j", "password")

    with driver.session() as session:
        n_nodes, n_edges = session.read_transaction(query_graph_info)
    driver.close()
    
    return n_nodes, n_edges


def query_graph_info(tx) :
    """  brief title.
    
    Arguments:
    arg1 - desc
    arg2 - desc

    Description:
    blablabla
    """

    n_nodes = tx.run("MATCH (n) RETURN COUNT(n)")
    n_nodes = n_nodes.single()[0]

    n_edges = tx.run("MATCH (n)-[r]->() RETURN COUNT(r)")
    n_edges = n_edges.single()[0]

    return n_nodes, n_edges


def is_db_initialize(NEO4J_ADDRESS) :
    """  brief title.
    
    Arguments:
    arg1 - desc
    arg2 - desc

    Description:
    blablabla
    """

    driver = connect_to_neo4j("bolt://" + NEO4J_ADDRESS + ":7687", "neo4j", "password")
    with driver.session() as session:
        result = session.read_transaction(query_db)
    driver.close()
    
    return result


def query_db(tx) :
    """  brief title.
    
    Arguments:
    arg1 - desc
    arg2 - desc

    Description:
    blablabla
    """

    result = tx.run("MATCH (n) RETURN COUNT(n)>0")

    result = result.single()[0]
    return result


def vuln_Neo4j(NEO4J_ADDRESS, vuln) :
    """  brief title.
    
    Arguments:
    arg1 - desc
    arg2 - desc

    Description:
    blablabla
    """

    driver = connect_to_neo4j("bolt://" + NEO4J_ADDRESS + ":7687", "neo4j", "password")
    with driver.session() as session:
        session.write_transaction(create_vuln, vuln)
    driver.close()


def create_vuln(tx, vuln) : 
    tx.run(vuln)


def parse_vuln_file() :
    """  brief title.
    
    Arguments:
    arg1 - desc
    arg2 - desc

    Description:
    blablabla
    """

    try :
        with open('./files/vulns.json', 'r') as vulns_file :
            vulns = json.load(vulns_file)

            # Return each vuln as a dictionary
            container_attacks = vulns['container_attacks']
            kernel_attacks = vulns['kernel_attacks'][0]
            engine_attacks = vulns['engine_attacks'][0]

            return container_attacks, kernel_attacks, engine_attacks

    except FileNotFoundError as error :
        print(error)
        exit(1)


def init_vuln(NEO4J_ADDRESS, vuln) : 
    """  brief title.
    
    Arguments:
    arg1 - desc
    arg2 - desc

    Description:
    blablabla
    """

    # FOR NOW I DO IT MANUALLY
    vuln_Neo4j(NEO4J_ADDRESS, vuln)


def initialize_Neo4j_db(NEO4J_ADDRESS) :
    """  brief title.
    
    Arguments:
    arg1 - desc
    arg2 - desc

    Description:
    blablabla
    """

    # If Neo4J is not empty
    if not is_db_initialize(NEO4J_ADDRESS) :

        print('Initializing the graph database...\n')

        # Retrieve Host info
        host = get_Infrastructure()

        # Initialize CAPs & syscalls, engines and kernel versions.
        init_Neo4j(NEO4J_ADDRESS)

        # Initialize Host
        host_Neo4j(NEO4J_ADDRESS, host)

        # Print graph info
        n_nodes, n_edges = graph_info(NEO4J_ADDRESS)
        print('Total: ' + str(n_nodes) + ' nodes and ' + str(n_edges) + ' relationships.\n')

        # Initialize Vulnerabilities
        init_vuln(NEO4J_ADDRESS, vuln1)
        init_vuln(NEO4J_ADDRESS, vuln2)
        init_vuln(NEO4J_ADDRESS, vuln3)

        # Print graph info
        # n_nodes, n_edges = graph_info(NEO4J_ADDRESS)
        # print('Total: ' + str(n_nodes) + ' nodes and ' + str(n_edges) + ' relationships.\n')


vuln1 = """
MERGE (m:MITRE:TACTIC {name: 'Privilege Escalation'})
MERGE (mm:MITRE:TECHNIQUE {name: 'Escape to Host'})
CREATE (c:CVE {name: 'Escape_1', CVSS_v3: gds.util.NaN(), ignore: false, needed: [], weight: -gds.util.infinity()})
CREATE (a:AND_NODE {key: 'AND_NODE', weight: 0, todo: 5, needed: [], pred: gds.util.NaN()})
CREATE (b:OR_NODE {key: 'OR_NODE', weight: -gds.util.infinity(), todo: 1, needed: [], pred: gds.util.NaN()})
MERGE (c)-[:USES]->(mm)
MERGE (mm)-[:LEADS_TO]->(m)
MERGE (b)-[:OR]->(c)
MERGE (a)-[:OR]->(b)
UNION
MATCH (b:OR_NODE {key: 'OR_NODE'})
MATCH (p:Permissions:Privileged)
MERGE (p)-[:OR]->(b)
UNION
MATCH (np:NewPriv {name: 'NewPriv'})
MATCH (a:AND_NODE {key: 'AND_NODE'})
MERGE (np)-[:AND]->(a)
UNION
MATCH (ro:NotReadOnly {name: 'NotReadOnly', object: 'Container'})
MATCH (a:AND_NODE {key: 'AND_NODE'})
MERGE (ro)-[:AND]->(a)
UNION
MATCH (c:Capability {name: 'CAP_SYS_ADMIN'})
MATCH (a:AND_NODE {key: 'AND_NODE'})
MERGE (c)-[:AND]->(a)
UNION
MATCH (s:SystemCall {name: 'mount'})
MATCH (a:AND_NODE {key: 'AND_NODE'})
MERGE (s)-[:AND]->(a)
UNION
MATCH (cc:ContainerConfig {name: 'root', type: 'user'})
MATCH (a:AND_NODE {key: 'AND_NODE'})
MERGE (cc)-[:AND]->(a)
"""

vuln2 = """
MERGE (m:MITRE:TACTIC {name: 'Privilege Escalation'})
MERGE (mm:MITRE:TECHNIQUE {name: 'Exploitation'})
CREATE (c:CVE {name: 'CVE-2022-0847'})
CREATE (b:OR_NODE {key: 'OR_NODE', vuln: 'vuln2', weight: -gds.util.infinity(), todo: 1, needed: [], pred: gds.util.NaN()})
MERGE (mm)-[:LEADS_TO]->(m)
MERGE (c)-[:USES]->(mm)
MERGE (b)-[:OR]->(c)
UNION 
MATCH (kv:KernelVersion {key: '5.8'})
MATCH (b:OR_NODE {key: 'OR_NODE', vuln: 'vuln2'})
MERGE (kv)-[:OR]->(b)
UNION
MATCH (kv:KernelVersion {key: '5.9'})
MATCH (b:OR_NODE {key: 'OR_NODE', vuln: 'vuln2'})
MERGE (kv)-[:OR]->(b)
UNION
MATCH (kv:KernelVersion {key: '5.10'})
MATCH (b:OR_NODE {key: 'OR_NODE', vuln: 'vuln2'})
MERGE (kv)-[:OR]->(b)
UNION
MATCH (kv:KernelVersion {key: '5.15'})
MATCH (b:OR_NODE {key: 'OR_NODE', vuln: 'vuln2'})
MERGE (kv)-[:OR]->(b)
UNION
MATCH (kv:KernelVersion {key: '5.16'})
MATCH (b:OR_NODE {key: 'OR_NODE', vuln: 'vuln2'})
MERGE (kv)-[:OR]->(b)
"""

vuln3 = """
MERGE (p:Permissions:Privileged {name: 'Privileged'})
MERGE (cc:ContainerConfig {name: 'root'})
MERGE (m:MITRE:TACTIC {name: 'Privilege Escalation'})
MERGE (mm:MITRE:TECHNIQUE {name: 'Exploitation'})
CREATE (c:CVE {name: 'CVE-2022-0185'})
CREATE (a:AND_NODE {key: 'AND_NODE', vuln: 'vuln3', name: 'and1', weight: 0, todo: 2, needed: [], pred: gds.util.NaN()})
CREATE (a1:AND_NODE {key: 'AND_NODE', vuln: 'vuln3', name: 'and2', weight: 0, todo: 2, needed: [], pred: gds.util.NaN()})
CREATE (b:OR_NODE {key: 'OR_NODE', vuln: 'vuln3', name: 'or1', weight: -gds.util.infinity(), todo: 1, needed: [], pred: gds.util.NaN()})
CREATE (b2:OR_NODE {key: 'OR_NODE', vuln: 'vuln3', name: 'or2', weight: -gds.util.infinity(), todo: 1, needed: [], pred: gds.util.NaN()})
MERGE (mm)-[:LEADS_TO]->(m)
MERGE (c)-[:USES]->(mm)
MERGE (a)-[:AND]->(c)
MERGE (b)-[:OR]->(a)
MERGE (b2)-[:OR]->(a)
UNION 
MATCH (b2:OR_NODE {key: 'OR_NODE', vuln: 'vuln3', name: 'or1'})
MATCH (p:Permissions:Privileged)
MERGE (p)-[:OR]->(b2)
UNION
MATCH (b2:OR_NODE {key: 'OR_NODE', vuln: 'vuln3', name: 'or1'})
MATCH (a1:AND_NODE {key: 'AND_NODE', vuln: 'vuln3', name: 'and2'})
MERGE (a1)-[:OR]->(b2)
UNION
MATCH (a1:AND_NODE {key: 'AND_NODE', vuln: 'vuln3', name: 'and2'})
MATCH (cc:ContainerConfig {name: 'root', type: 'user'})
MERGE (cc)-[:AND]->(a1)
UNION
MATCH (a1:AND_NODE {key: 'AND_NODE', vuln: 'vuln3', name: 'and2'})
MATCH (cap:Capability {name: 'CAP_SYS_ADMIN'})
MERGE (cap)-[:AND]->(a1)
UNION
MATCH (kv:KernelVersion {key: '5.1'})
MATCH (b:OR_NODE {key: 'OR_NODE', vuln: 'vuln3', name: 'or2'})
MERGE (kv)-[:OR]->(b)
UNION
MATCH (kv:KernelVersion {key: '5.2'})
MATCH (b:OR_NODE {key: 'OR_NODE', vuln: 'vuln3', name: 'or2'})
MERGE (kv)-[:OR]->(b)
UNION
MATCH (kv:KernelVersion {key: '5.3'})
MATCH (b:OR_NODE {key: 'OR_NODE', vuln: 'vuln3', name: 'or2'})
MERGE (kv)-[:OR]->(b)
UNION
MATCH (kv:KernelVersion {key: '5.4'})
MATCH (b:OR_NODE {key: 'OR_NODE', vuln: 'vuln3', name: 'or2'})
MERGE (kv)-[:OR]->(b)
UNION
MATCH (kv:KernelVersion {key: '5.5'})
MATCH (b:OR_NODE {key: 'OR_NODE', vuln: 'vuln3', name: 'or2'})
MERGE (kv)-[:OR]->(b)
UNION
MATCH (kv:KernelVersion {key: '5.6'})
MATCH (b:OR_NODE {key: 'OR_NODE', vuln: 'vuln3', name: 'or2'})
MERGE (kv)-[:OR]->(b)
UNION
MATCH (kv:KernelVersion {key: '5.7'})
MATCH (b:OR_NODE {key: 'OR_NODE', vuln: 'vuln3', name: 'or2'})
MERGE (kv)-[:OR]->(b)
UNION
MATCH (kv:KernelVersion {key: '5.8'})
MATCH (b:OR_NODE {key: 'OR_NODE', vuln: 'vuln3', name: 'or2'})
MERGE (kv)-[:OR]->(b)
UNION
MATCH (kv:KernelVersion {key: '5.9'})
MATCH (b:OR_NODE {key: 'OR_NODE', vuln: 'vuln3', name: 'or2'})
MERGE (kv)-[:OR]->(b)
UNION
MATCH (kv:KernelVersion {key: '5.10'})
MATCH (b:OR_NODE {key: 'OR_NODE', vuln: 'vuln3', name: 'or2'})
MERGE (kv)-[:OR]->(b)
UNION
MATCH (kv:KernelVersion {key: '5.11'})
MATCH (b:OR_NODE {key: 'OR_NODE', vuln: 'vuln3', name: 'or2'})
MERGE (kv)-[:OR]->(b)
UNION
MATCH (kv:KernelVersion {key: '5.12'})
MATCH (b:OR_NODE {key: 'OR_NODE', vuln: 'vuln3', name: 'or2'})
MERGE (kv)-[:OR]->(b)
UNION
MATCH (kv:KernelVersion {key: '5.13'})
MATCH (b:OR_NODE {key: 'OR_NODE', vuln: 'vuln3', name: 'or2'})
MERGE (kv)-[:OR]->(b)
UNION
MATCH (kv:KernelVersion {key: '5.14'})
MATCH (b:OR_NODE {key: 'OR_NODE', vuln: 'vuln3', name: 'or2'})
MERGE (kv)-[:OR]->(b)
UNION
MATCH (kv:KernelVersion {key: '5.15'})
MATCH (b:OR_NODE {key: 'OR_NODE', vuln: 'vuln3', name: 'or2'})
MERGE (kv)-[:OR]->(b)
UNION
MATCH (kv:KernelVersion {key: '5.16'})
MATCH (b:OR_NODE {key: 'OR_NODE', vuln: 'vuln3', name: 'or2'})
MERGE (kv)-[:OR]->(b)
"""