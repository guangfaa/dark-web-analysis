package number;
import org.apache.tinkerpop.gremlin.driver.Client;
import org.apache.tinkerpop.gremlin.driver.Cluster;
import org.apache.tinkerpop.gremlin.process.traversal.dsl.graph.GraphTraversalSource;
import org.apache.tinkerpop.gremlin.structure.Graph;
import org.apache.tinkerpop.gremlin.structure.Vertex;
import org.apache.tinkerpop.gremlin.driver.remote.DriverRemoteConnection;
import org.apache.tinkerpop.gremlin.process.traversal.AnonymousTraversalSource;
import org.apache.tinkerpop.gremlin.process.traversal.dsl.graph.GraphTraversal;
import org.apache.tinkerpop.gremlin.process.traversal.dsl.graph.GraphTraversalSource;
import org.apache.tinkerpop.gremlin.process.traversal.dsl.graph.__;
import org.apache.tinkerpop.gremlin.process.traversal.P;
import org.janusgraph.core.JanusGraph;
import org.janusgraph.core.JanusGraphFactory;
import org.janusgraph.core.schema.JanusGraphManagement;
import org.janusgraph.core.schema.JanusGraphIndex;
import org.janusgraph.core.schema.SchemaAction;
import org.janusgraph.core.JanusGraphTransaction;
import org.janusgraph.core.*;
import org.janusgraph.graphdb.database.StandardJanusGraph;
import org.janusgraph.graphdb.database.util.*;
import org.apache.tinkerpop.gremlin.structure.Direction;

import java.util.stream.Collectors;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.stream.Stream;
import java.util.*;

public class number {
    public static void main(String[] args) {
        batchMethod();
    }

    public static void batchMethod(){
        AtomicInteger minDegree = new AtomicInteger((int) addProperty());
        //  String propertyFile = "C:/Users/10465/Desktop/platform/janusgraph/janusgraph-0.5.2/conf/janusgraph-berkeleyje.properties";
        String propertyFile = "/public/home/blockchain_2/slave1/janus-eth-tools/experiment/janusgraph-hbase-solr-bnb-experiment.properties";
        JanusGraph graph = JanusGraphFactory.open(propertyFile);
        GraphTraversalSource g = graph.traversal();
        boolean kcore_status = g.V().has("un_kcore_status", 0).hasNext();
        while (kcore_status) {
            List<Long> vertices_list = new ArrayList<>();
            for (int curDegree = 0; curDegree <= minDegree.get(); ++curDegree) {
                List<Long> partialList = g.V().has("un_kcore_status", 0).has("un_kcore_degree", curDegree)
                    .id()
                    .toList()
                    .stream()
                    .map(id -> ((Number) id).longValue())
                    .collect(Collectors.toList());
                vertices_list.addAll(partialList);
            }
            if (!vertices_list.isEmpty()) {
                g.tx().begin();
                g.V(vertices_list).property("un_kcore_status", 1).iterate();
                g.V(vertices_list).property("un_kcore", minDegree.get()).iterate();
                g.tx().commit();
                for(Long vertex : vertices_list){
                    System.out.println(vertex);
                    List<Long> adj_list = g.V(vertex).both().dedup()
                            .id()
                            .toList()
                            .stream()
                            .map(id -> ((Number) id).longValue())
                            .collect(Collectors.toList());
                    // List<Vertex> adj_list = g.V(vertex).both().dedup().toList();
                    for (Long adj : adj_list) {
                        Integer degree = (int) g.V(adj).values("un_kcore_degree").next();
                        Integer newDegree = degree - 1;
                        g.tx().begin();
                        g.V(adj).property("un_kcore_degree", newDegree).iterate();
                        g.tx().commit();
                    }   
                }
            }
            else {
                minDegree.incrementAndGet();
                System.out.println(minDegree);
            }
            kcore_status = g.V().has("un_kcore_status", 0).hasNext();
        }
        g.tx().commit();
        graph.close();
    }

    private static long addProperty(){
        //  String propertyFile = "C:/Users/10465/Desktop/platform/janusgraph/janusgraph-0.5.2/conf/janusgraph-berkeleyje.properties";
        String propertyFile = "/public/home/blockchain_2/slave1/janus-eth-tools/experiment/janusgraph-hbase-solr-bnb-experiment.properties";
        JanusGraph graph = JanusGraphFactory.open(propertyFile);

        // index
        JanusGraphManagement m = graph.openManagement();
        PropertyKey un_kcore_degree = m.getPropertyKey("un_kcore_degree");
        if (un_kcore_degree == null){
            un_kcore_degree = m.makePropertyKey("un_kcore_degree").dataType(Integer.class).make();
        }
        JanusGraphIndex un_degIndex = m.getGraphIndex("un_degIndex");
        if (un_degIndex == null){
            m.buildIndex("un_degIndex", Vertex.class).addKey(un_kcore_degree).buildCompositeIndex();
        }
        PropertyKey un_kcore_status = m.getPropertyKey("un_kcore_status");
        if (un_kcore_status == null){
            un_kcore_status = m.makePropertyKey("un_kcore_status").dataType(Integer.class).make();
        }
        JanusGraphIndex un_satIndex = m.getGraphIndex("un_satIndex");
        if (un_satIndex == null){
            m.buildIndex("un_satIndex", Vertex.class).addKey(un_kcore_status).buildCompositeIndex();
        }
        PropertyKey un_kcore = m.getPropertyKey("un_kcore");
        if (un_kcore == null){
            un_kcore = m.makePropertyKey("un_kcore").dataType(Integer.class).make();
        }
        JanusGraphIndex un_kIndex = m.getGraphIndex("un_kIndex");
        if (un_kIndex == null){
            m.buildIndex("un_kIndex", Vertex.class).addKey(un_kcore).buildCompositeIndex();
        }
        m.commit();

        final long[] min_degree = {Long.MAX_VALUE};
        GraphTraversalSource g = graph.traversal();
        g.V().forEachRemaining(vertex -> {
            long degree = g.V(vertex).both().dedup().count().next();
            if (degree < min_degree[0]){
                min_degree[0] = degree;
            }
            JanusGraphTransaction tx = graph.newTransaction();
            Vertex txVertex = tx.vertices(vertex.id()).next();
            txVertex.property("un_kcore_degree", (int) degree);
            txVertex.property("un_kcore_status", 0);
            System.out.println(txVertex.id());
            tx.commit();
        });

        graph.close();
        System.out.println("add property finished");
        return min_degree[0];
    }
}