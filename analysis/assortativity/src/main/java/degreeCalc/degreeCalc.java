package degreeCalc;

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

import java.io.BufferedWriter;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.List;

public class degreeCalc {
    private static int count = 0;
    public static void main(String[] args) {
        String mainGraph = "/public/home/blockchain_2/slave1/darknet-test/janusgraph-hbase-solr.properties";
        
        JanusGraph graph = JanusGraphFactory.open(mainGraph);

        // List<Vertex> nodes = getRandomNodes(graph, 10000);
        // System.out.println("Sampled nodes: " + nodes.size());

        GraphTraversalSource g = graph.traversal();
        JanusGraph graph2 = JanusGraphFactory.open(mainGraph);
        GraphTraversalSource g2 = graph2.traversal();
        try (BufferedWriter writer = Files.newBufferedWriter(Paths.get("out2-inAndout-neighbor_degrees.csv"))) {
            writer.write("NodeID;Degree;NeighborInDegrees;NeighborOutDegrees\n");
            g.V().forEachRemaining(node -> {
                if (count >= 10000) {
                    System.out.println("Done!!!Done!!!Done!!!Done!!!Done!!!"); 
                    return;
                }
                List<Object[]> neighborData = g2.V(node)
                    .out() // 获取所有相连节点（入边和出边的邻居） 改这里就是入节点还是出节点
                    .dedup() // 去重
                    .project("vertex", "in", "out") // 同时获取顶点和度数
                    .by()      // 顶点对象
                    .by(__.inE().count()) // 入度
                    .by(__.outE().count()) // 出度
                    .toStream()
                    .map(t -> new Object[]{
                        t.get("vertex"), 
                        t.get("in"), 
                        t.get("out")
                    })
                    .collect(Collectors.toList());

                if (neighborData.isEmpty()) {
                    // writer.write(node.id().toString() + ";0;[];[]" + "\n");
                    System.out.println("Empty outvertex");
                    return;
                }

                // // 计算统计指标
                // int totalIn = neighborData.stream().mapToInt(t -> (int)t[1]).sum();
                // int totalOut = neighborData.stream().mapToInt(t -> (int)t[2]).sum();
                // double avgIn = totalIn * 1.0 / neighborData.size();
                // double avgOut = totalOut * 1.0 / neighborData.size();

                // // 生成ID和度数列表
                // String neighborIds = neighborData.stream()
                //     .map(t -> ((Vertex)t[0]).id().toString())
                //     .collect(Collectors.joining(";"));
                
                String inDegrees = neighborData.stream()
                    .map(t -> t[1].toString())
                    .collect(Collectors.joining(","));
                
                String outDegrees = neighborData.stream()
                    .map(t -> t[2].toString())
                    .collect(Collectors.joining(","));

                // 手动构建CSV行
                String csvLine = String.join(";",
                    node.id().toString(),
                    String.valueOf(neighborData.size()),
                    // String.valueOf(avgIn),
                    // String.valueOf(avgOut),
                    // String.valueOf(totalIn),
                    // String.valueOf(totalOut),
                    // "\"" + neighborIds + "\"",  // 用引号包裹包含分隔符的字段
                    "[" + inDegrees + "]",
                    "[" + outDegrees + "]"
                );
                try {
                    writer.write(csvLine + "\n");
                } catch (Exception e) {
                    e.printStackTrace(); // 打印错误堆栈
                }
                System.out.println(csvLine);
                count = count + 1;
            });
        } catch (Exception e) {
            e.printStackTrace(); // 打印错误堆栈
        }

        graph.close();
        // graph2.close();
    }

    // private static final int BATCH_SIZE = 2000;  // 每批次生成的ID数量
    // private static final long COEFFICIENT_I = 4915200000L;
    // private static final long COEFFICIENT_J = 4096L;

    // private static List<Vertex> getRandomNodes(JanusGraph graph, int sampleSize) {
    //     GraphTraversalSource g = graph.traversal();
    //     Random random = new Random();
    //     Set<Vertex> results = new LinkedHashSet<>(sampleSize);

    //     while (results.size() < sampleSize) {
    //         try {
    //             // 批量生成随机ID（优化内存：直接生成对象数组）
    //             Object[] ids = new Object[BATCH_SIZE];
    //             for (int k = 0; k < BATCH_SIZE; k++) {
    //                 int i = random.nextInt(101);    // 0~100
    //                 int j = random.nextInt(10000) + 1; // 1~10000
    //                 ids[k] = COEFFICIENT_I * i + COEFFICIENT_J * j;
    //             }

    //             // // 批量查询节点（自动过滤不存在ID）
    //             // List<Vertex> nodes = g.V(ids).toList();

    //             // 批量查询并过滤无出边的节点
    //             List<Vertex> nodes = g.V(ids)
    //                 .where(__.in().count().is(P.gt(0))) // 使用P.gt(0)
    //                 .toList();

    //             // 去重并加入结果集
    //             nodes.stream()
    //                 .filter(v -> !results.contains(v))
    //                 .forEach(results::add);

    //             // System.out.println(nodes);

    //             // 提前终止条件
    //             if (results.size() >= sampleSize) break;
    //         } catch (Exception e) {
    //             e.printStackTrace(); // 打印错误堆栈
    //         }
    //     }

    //     return new ArrayList<>(results).subList(0, Math.min(sampleSize, results.size()));
    // }
}