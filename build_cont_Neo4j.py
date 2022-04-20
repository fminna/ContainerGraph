from neo4j import GraphDatabase


def connect_to_neo4j(uri, user, password) :
    """  brief title.
    
    Arguments:
    arg1 - desc
    arg2 - desc

    Description:
    blablabla
    """

    driver = GraphDatabase.driver(uri, auth=(user, password))
    return driver


def cont_Neo4j_chart(NEO4J_ADDRESS, cont) :
    """  brief title.
    
    Arguments:
    arg1 - desc
    arg2 - desc

    Description:
    blablabla
    """

    driver = connect_to_neo4j("bolt://" + NEO4J_ADDRESS + ":11005", "neo4j", "password")
    
    with driver.session() as session:

        session.write_transaction(create_cont_node, cont)
        session.write_transaction(create_cconfig_nodes, cont)
        session.write_transaction(create_cconfig_relationships, cont)

        if cont.permissions.profile == 'docker-privileged' :
            session.write_transaction(create_permissions_node)
            session.write_transaction(create_perm_relationships, cont) 
        
        else :
            session.write_transaction(create_sec_prof_nodes, cont)
            session.write_transaction(create_prof_relationships, cont) 

        session.write_transaction(create_cont_relationships, cont) 

    driver.close()


def create_cconfig_nodes(tx, cont) :
    """  brief title.
    
    Arguments:
    arg1 - desc
    arg2 - desc

    Description:
    blablabla
    """

    # For each docker run arg (e.g. user, volume, etc.) create a node 
    for key in cont.cconfig.fields :
        value = cont.cconfig.fields[key]

        if not key == 'name' :
            if type(value) == list :
                query = "MERGE (cc:ContainerConfig {name: $key, value: $value})"
                tx.run(query, key = key, value = value)

            else :
                query = "MERGE (cc:ContainerConfig {name: $value, type: $type})"
                tx.run(query, type = key, value = value)


def create_cconfig_relationships(tx, cont) :
    """  brief title.
    
    Arguments:
    arg1 - desc
    arg2 - desc

    Description:
    blablabla
    """

    # For each docker run arg (e.g. user, volume, etc.) create a node 
    for key in cont.cconfig.fields :
        value = cont.cconfig.fields[key]

        if not key == 'name' :
            if type(value) == list :
                tx.run("MATCH (c:Container:Docker {cont_id: $cont_id}) "
                       "MATCH (cc:ContainerConfig {name: $key, value: $value}) "
                       "MERGE (c)-[:HAS]->(cc) ",
                       cont_id = cont.cont_id, key = key, value = value
                )

            else :
                tx.run("MATCH (c:Container:Docker {cont_id: $cont_id}) "
                       "MATCH (cc:ContainerConfig {name: $value, type: $type}) "
                       "MERGE (c)-[:HAS]->(cc) ",
                       cont_id = cont.cont_id, type = key, value = value
                )


def create_permissions_node(tx) :
    """  brief title.
    
    Arguments:
    arg1 - desc
    arg2 - desc

    Description:
    blablabla
    """

    tx.run("MERGE (p:PrivPermissions {name: 'PrivPermissions', object: 'Container'})") 


def create_sec_prof_nodes(tx, cont) :
    """  brief title.
    
    Arguments:
    arg1 - desc
    arg2 - desc

    Description:
    blablabla
    """

    tx.run("MERGE (aa:AppArmor {name: 'AppArmor', profile: $profile, object: 'Container'})", profile = cont.permissions.profile)
    tx.run("MERGE (sc:SecComp {name: 'SecComp', profile: $profile, object: 'Container'})", profile = cont.permissions.profile)


def create_prof_relationships(tx, cont) :
    """  brief title.
    
    Arguments:
    arg1 - desc
    arg2 - desc

    Description:
    blablabla
    """

    tx.run("MATCH (c:Container:Docker {cont_id: $cont_id}) "
        "MATCH (aa:AppArmor {name: 'AppArmor', profile: $profile}) "
        "MERGE (c)-[:HAS]->(aa) ",
        cont_id = cont.cont_id, profile = cont.permissions.profile
    )

    tx.run("MATCH (c:Container:Docker {cont_id: $cont_id}) "
        "MATCH (sc:SecComp {name: 'SecComp', profile: $profile}) "
        "MERGE (c)-[:HAS]->(sc) ",
        cont_id = cont.cont_id, profile = cont.permissions.profile
    )

    for cap in cont.permissions.caps :
        tx.run("MATCH (aa:AppArmor {name: 'AppArmor', profile: $profile}) "
           "MATCH (cap:Capability {name: '" + cap + "'})"
           "MERGE (aa)-[:HAS]->(cap) "
           , profile = cont.permissions.profile
        )

    for syscall in cont.permissions.syscalls :
        tx.run("MATCH (sc:SecComp {name: 'SecComp', profile: $profile}) "
           "MATCH (sysc:SystemCall {name: '" + syscall + "'})"
           "MERGE (sc)-[:HAS]->(sysc) "
           , profile = cont.permissions.profile
        )


def create_perm_relationships(tx, cont) :
    """  brief title.
    
    Arguments:
    arg1 - desc
    arg2 - desc

    Description:
    blablabla
    """

    tx.run("MATCH (c:Container:Docker {cont_id: $cont_id}) "
        "MATCH (pp:PrivPermissions {name: 'PrivPermissions', object: 'Container'}) "
        "MERGE (c)-[:HAS]->(pp) ",
        cont_id = cont.cont_id
    )

    for cap in cont.permissions.caps :
        tx.run("MATCH (pp:PrivPermissions {name: 'PrivPermissions', object: 'Container'}) "
           "MATCH (cap:Capability {name: '" + cap + "'})"
           "MERGE (pp)-[:HAS]->(cap) "
           , profile = cont.permissions.profile
        )

    for syscall in cont.permissions.syscalls :
        tx.run("MATCH (pp:PrivPermissions {name: 'PrivPermissions', object: 'Container'}) "
           "MATCH (sysc:SystemCall {name: '" + syscall + "'})"
           "MERGE (pp)-[:HAS]->(sysc) "
           , profile = cont.permissions.profile
        )


def create_cont_node(tx, cont) :
    """  brief title.
    
    Arguments:
    arg1 - desc
    arg2 - desc

    Description:
    blablabla
    """

    tx.run("MERGE (c:Container:Docker {name: $name, cont_id: $cont_id, img_id: $img_id, start_t: $start_t, status: $status})", cont_id = cont.cont_id, img_id = cont.img_id, name = cont.name, start_t = cont.start_t, status = cont.status) 


def create_cont_relationships(tx, cont) :
    """  brief title.
    
    Arguments:
    arg1 - desc
    arg2 - desc

    Description:
    blablabla
    """

    tx.run("MATCH (de:DockerEngine)-[:RUNS_ON_TOP]->(h:LinuxHost) "
           "MATCH (c:Container:Docker {cont_id: $cont_id}) "
           "MERGE (de)-[:RUNS]->(c) "
           "UNION "
           "MATCH (c:Container:Docker {cont_id: $cont_id}) "
           "MATCH (i:Image:Docker {img_id: $img_id})  "
           "MERGE (c)-[:INSTANCIATE]->(i) ", 
           cont_id = cont.cont_id, img_id = cont.img_id
    )

