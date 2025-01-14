from Node import Node
from network import generate_eventrates, create_random_tree,generate_events
from graph import create_fog_graph
from graph import draw_graph
from allPairs import populate_allPairs
from queryworkload import generate_workload
from selectivity import initialize_selectivities
from write_config_single import generate_config_buffer
from singleSelectivities import initializeSingleSelectivity
from helper.parse_network import initialize_globals


class INES():
    allPais: list
    network: list[Node]
    eventrates: list[list[int]]
    query_workload = None
    selectivities = None
    selectivitiesExperimentData = None
    primitiveEvents: list[int]
    config_single: None
    single_selectivity = None

    "Helper Variables from different Files - namespace issues"
    h_network_data = None
    h_rates_data = None
    h_primEvents = None
    h_instances=None
    h_nodes = None
    h_projlist = None
    h_projrates = None
    h_projsPerQuery = None
    h_sharedProjectionsDict = None
    h_sharedProjectionsList = None


    def __init__(self, nwSize: int, node_event_ratio: float, num_eventtypes: int, eventskew: float, max_partens: int, query_size: int, query_length:int):
        from projections import generate_all_projections
        self.eventrates = generate_eventrates(eventskew,num_eventtypes)
        self.primitiveEvents= generate_events(self.eventrates,node_event_ratio)
        root, self.network = create_random_tree(nwSize,self.eventrates,node_event_ratio,max_partens) 
        self.graph = create_fog_graph(self.network)
        self.allPais = populate_allPairs(self.graph)
        self.query_workload = generate_workload(query_size,query_length,self.primitiveEvents)
        self.selectivities,self.selectivitiesExperimentData = initialize_selectivities(self.primitiveEvents)
        self.config_single = generate_config_buffer(self.network,self.query_workload,self.selectivities)
        self.single_selectivity = initializeSingleSelectivity(self.config_single, self.query_workload)

        #This is important to variious files afterwards
        self.h_network_data,self.h_rates_data,self.h_primEvents,self.h_instances,self.h_nodes = initialize_globals(self.network)
        self.h_projlist,self.h_projrates,self.h_projsPerQuery,self.h_sharedProjectionsDict,self.h_sharedProjectionsList = generate_all_projections(self)

my_ines = INES(12,0.5,6,0.3,2,3,5)

print(my_ines.query_workload)
print(my_ines.config_single)
print(my_ines.single_selectivity)
print(my_ines.h_projlist)
#print(my_ines.allPais)
#draw_graph(my_ines.graph)

# for i in my_ines.network:
#     print(i)