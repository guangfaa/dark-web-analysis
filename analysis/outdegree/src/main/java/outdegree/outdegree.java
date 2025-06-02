package outdegree;

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
import org.janusgraph.core.schema.JanusGraphManagement;
import org.janusgraph.core.schema.JanusGraphIndex;
import org.janusgraph.core.schema.SchemaAction;
import org.janusgraph.core.*;
import org.janusgraph.graphdb.database.StandardJanusGraph;
import org.janusgraph.graphdb.database.util.*;
import org.apache.tinkerpop.gremlin.structure.Direction;

import java.util.stream.Collectors;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.stream.Stream;
import java.lang.reflect.Array;
import java.util.*;
import java.util.concurrent.*;
import java.util.stream.IntStream;

public class outdegree {
    public static void main(String[] args) {
        String mainGraph = "/public/home/blockchain_2/slave1/darknet-test/janusgraph-hbase-solr.properties";
        
        JanusGraph graph = JanusGraphFactory.open(mainGraph);
        GraphTraversalSource g = graph.traversal();
        JanusGraph graph2 = JanusGraphFactory.open(mainGraph);
        GraphTraversalSource g2 = graph2.traversal();

        // Map<Long, Long> degreeCount = new HashMap<>();

        // 添加hasLabel过滤，仅处理标签为dark的节点
        g.V().forEachRemaining(vertex -> {
            Object bulkLoaderId = vertex.property("bulkLoader.vertex.id").orElse(null);
            if ("dark".equals(vertex.label())) {  // 检查顶点标签是否为dark
                long degree = g2.V(vertex).outE().count().next();
                if (degree >= 700 && degree <= 1000) {
                System.out.println(bulkLoaderId+"度数"+degree);
                }
                // degreeCount.merge(degree, 1L, Long::sum);
            }
        });

        // System.out.println("Dark节点入度分布统计:");
        // degreeCount.forEach((degree, count) -> {
        //     System.out.println("入度 " + degree + " 的节点数量: " + count);
        // });

        graph.close();
        graph2.close();
    }
}