package step;

import org.apache.tinkerpop.gremlin.process.traversal.dsl.graph.GraphTraversalSource;
import org.apache.tinkerpop.gremlin.structure.Vertex;
import org.janusgraph.core.JanusGraph;
import org.janusgraph.core.JanusGraphFactory;
import java.util.*;
import static org.apache.tinkerpop.gremlin.process.traversal.dsl.graph.__.*;

public class step {

    public static void main(String[] args) {
        String configFile = "/public/home/blockchain_2/slave1/darknet-test/janusgraph-hbase-solr2.properties";
        JanusGraph graph = null;
        JanusGraph graph2 = null;
        try {
            graph = JanusGraphFactory.open(configFile);
            GraphTraversalSource g = graph.traversal();
            graph2 = JanusGraphFactory.open(configFile);
            GraphTraversalSource g2 = graph2.traversal();

            // ██████████████████████████████████████████████████████████████
            // 改动点：预加载所有需要统计的节点（保持后续处理逻辑完全不变）
            List<Vertex> targetVertices = g2.V()
                .hasLabel("dark")
                .where(outE().limit(1))
                .limit(100)  // 一次性获取100个符合条件的节点
                .toList();
            // ██████████████████████████████████████████████████████████████

            // 保持原有的循环结构（仅将分页查询改为从列表获取）
            for (int i = 0; i < targetVertices.size(); i++) {
                Vertex startVertex = targetVertices.get(i); // 从预加载列表获取节点

                System.out.println("\n=== 节点 " + (i+1) + "/" + targetVertices.size() + " ===");
                System.out.println("节点ID: " + startVertex.id());

                // 完全保持原有的BFS统计逻辑
                try {
                    Map<Integer, Long> stepCounts = bfsWithTimeout(g, startVertex, 6, 120_000);
                    printStepResults(stepCounts);
                } catch (Exception e) {
                    System.err.println("节点 " + startVertex.id() + " 统计失败: " + e.getMessage());
                }

                // 保持原有的资源释放和间隔控制
                g.close();
                Thread.sleep(1000);
            }

        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            if (graph != null) graph.close();
        }
    }

    // ▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼ 以下两个方法完全未改动 ▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼
    private static Map<Integer, Long> bfsWithTimeout(GraphTraversalSource g, 
                                                   Vertex startVertex, 
                                                   int maxSteps, 
                                                   long timeoutMs) throws Exception {
        Map<Integer, Long> stepCounts = new LinkedHashMap<>();
        Set<Object> visited = new HashSet<>();
        Deque<Vertex> currentLayer = new LinkedList<>();

        visited.add(startVertex.id());
        currentLayer.add(startVertex);
        stepCounts.put(0, 1L);

        long startTime = System.currentTimeMillis();
        for (int step = 1; step <= maxSteps; step++) {
            if (System.currentTimeMillis() - startTime > timeoutMs) {
                throw new Exception("BFS遍历超时，已超过 " + timeoutMs + "ms");
            }

            if (currentLayer.isEmpty()) break;

            List<Object> batchIds = new ArrayList<>();
            currentLayer.forEach(v -> batchIds.add(v.id()));

            List<Vertex> neighbors = g.V(batchIds.toArray())
                .out()
                .dedup()
                .toList();

            Set<Vertex> nextLayer = new HashSet<>();
            for (Vertex neighbor : neighbors) {
                if (!visited.contains(neighbor.id())) {
                    visited.add(neighbor.id());
                    nextLayer.add(neighbor);
                }
            }

            stepCounts.put(step, (long) nextLayer.size());
            currentLayer.clear();
            currentLayer.addAll(nextLayer);
        }
        return stepCounts;
    }

    private static void printStepResults(Map<Integer, Long> stepCounts) {
        System.out.println("+-------+------------+");
        System.out.println("| 步数  | 新到达节点数 |");
        System.out.println("+-------+------------+");
        stepCounts.forEach((step, count) -> {
            System.out.printf("| %5d | %10d |\n", step, count);
        });
        System.out.println("+-------+------------+");
    }
}